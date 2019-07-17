# This monkey patch is necesary for celery asynchronous then
import gevent.monkey
gevent.monkey.patch_all()

import json
import uuid
from redis import Redis

from flask import Flask, url_for
from flask import request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_sse import sse

from timeit import default_timer as timer

from .responses import JSON

from newslyzer.workers.celery import app
from newslyzer.workers.workflow import workflow

redis = Redis(host='localhost', port=6379)

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

def workflow_failed(flask, url):
    def callback(error):
        redis.set('url:{}:result'.format(url), json.dumps(error.result))
        redis.set('url:{}:status'.format(url), 'failed')
        with flask.app_context():
            sse.publish({ 'url': url, 'status': 'failed', 'error': error.message }, channel=url)

    return callback

def workflow_done(flask, url):
    def callback(result):
        redis.set('url:{}:result'.format(url), json.dumps(result.result))
        redis.set('url:{}:status'.format(url), 'processed')
        with flask.app_context():
            sse.publish({ 'url': url, 'status': 'processed' }, channel=url)

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

        # URL is already processed
        if status == 'processed':
            result = redis.get('url:{}:result'.format(url))
            response = JSON(response=result.decode('utf-8'))
        else:
            if status == processing_value:
                redis.set('url:{}:status'.format(url), processing_value)
                workflow(url).then(workflow_done(self.app, url), workflow_failed(self.app, url))

            result = {
                'status': 'in_progress',
                'notifications': url_for("sse.stream", channel=url),
            }
            response = JSON(response=result)

        return response


def setup_app():
    flask = Flask(__name__)
    # flask.debug = True

    api = Api(flask)
    api.add_resource(HelloResource, '/')
    api.add_resource(ArticleResource, '/article', resource_class_kwargs={
        'logger': flask.logger,
        'app': flask
    })

    flask.config['REDIS_URL'] = 'redis://localhost'
    flask.register_blueprint(sse, url_prefix='/notifications')

    CORS(app=flask, supports_credentials=True)
    return flask


if __name__ == '__main__':
    flask = setup_app()
    flask.run()
