# This monkey patch is necesary for celery asynchronous then
import gevent.monkey
gevent.monkey.patch_all()

import json
import uuid
from redis import Redis

from flask import Flask, Blueprint, request, url_for, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_sse import sse

from timeit import default_timer as timer

from .config import redis_connection, redis_host, redis_port, wordcloud_path

from .responses import JSON
from .workflow import start_worker

redis = Redis(host=redis_host, port=int(redis_port))

def parse_request():
    parser = reqparse.RequestParser()
    parser.add_argument('url', required=True)
    parser.add_argument('engine', type=str)
    return parser.parse_args()

class HelloResource(Resource):
    def get(self):
        result = {
            'status': 'OK',
            'time': str(timer())
        }
        return JSON(response=result)

def workflow_failed(flask, url, pubsub_thread):
    def callback(error):
        redis.set('url:{}:result'.format(url), json.dumps(error.result))
        redis.set('url:{}:status'.format(url), 'failed')
        with flask.app_context():
            sse.publish({ 'url': url, 'status': 'failed', 'error': error.message }, channel=url)

        pubsub_thread.stop()

    return callback

def workflow_done(flask, url, pubsub_thread):
    def callback(result):
        print('Workflow done {}'.format(url))
        redis.set('url:{}:result'.format(url), json.dumps(result.result))
        redis.set('url:{}:status'.format(url), 'processed')
        with flask.app_context():
            sse.publish({ 'url': url, 'status': 'processed' }, channel=url)

        pubsub_thread.stop()

    return callback

def workflow_progress(flask, url):
    def callback(progress):
        with flask.app_context():
            sse.publish({ 'url': url, 'status': 'in_progress', 'progress': progress['data'].decode('utf-8') }, channel=url)

    return callback

class ArticleResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.app = kwargs.get('app')

    def get(self):
        print("!! Request received")

        # Creates an unique id so we know that we're asigned to launch the workflo
        self_uuid = str(uuid.uuid4())

        # Process request parameters
        args = parse_request()
        url = args.get('url')

        # Remove query parameters
        if ('?' in url):
            url = url[:url.find('?')]

        processing_value = 'processing:{}'.format(self_uuid)
        status_bytes = redis.get('url:{}:status'.format(url))

        if status_bytes:
            status = status_bytes.decode('utf-8')
        else:
            status = processing_value

        print('url:{}:status ==> {}'.format(url, status))
        sse.publish({ 'url': url, 'status': 'in_progress' }, channel=url)

        # URL is already processed
        if status == 'processed':
            result = redis.get('url:{}:result'.format(url))
            response = JSON(response=result.decode('utf-8'))
        else:
            if status == processing_value:
                redis.set('url:{}:status'.format(url), processing_value)
                redis.set('url:{}:completed'.format(url), 0)
                pubsub = redis.pubsub()
                pubsub.subscribe(**{ 'url:{}:progress'.format(url): workflow_progress(self.app, url) })
                pubsub_thread = pubsub.run_in_thread(sleep_time=0.001)
                start_worker(url).then(
                    workflow_done(self.app, url, pubsub_thread),
                    workflow_failed(self.app, url, pubsub_thread))

            result = {
                'status': 'in_progress',
                'notifications': url_for("sse.stream", channel=url, _external=True),
            }
            response = JSON(response=result)

        return response

def index():
    url = request.args.get('url')
    result = redis.get('url:{}:result'.format(url))

    if result:
        data = json.loads(result)
        title = 'Sentiment Analisys from "{}"'.format(data['metadata'].get('sourceName', data['metadata']['sourceUrl']))
        description = 'We\'ve analyzed this news article: "{}"'.format(data['metadata']['title'])
        image = wordcloud_path + '/' + data['wordcloud']

        return render_template(
            "index.html",
            url=url,
            title=title,
            description=description,
            image=image)
    else:
        return render_template("index.html", url=url)

def setup_app():
    flask = Flask(__name__)
    # flask.debug = True
    flask.add_url_rule('/', 'index', view_func=index)

    flask.config['REDIS_URL'] = redis_connection
    flask.register_blueprint(sse, url_prefix='/stream')

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(HelloResource, '/')
    api.add_resource(ArticleResource, '/article', resource_class_kwargs={
        'logger': flask.logger,
        'app': flask
    })

    flask.register_blueprint(api_bp, url_prefix='/api')

    CORS(app=flask, supports_credentials=True)
    return flask


if __name__ == '__main__':
    flask = setup_app()
    flask.run()
