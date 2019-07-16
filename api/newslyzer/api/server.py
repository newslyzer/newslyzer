from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from timeit import default_timer as timer

from .cache import CacheService
from .responses import JSON

from newslyzer.workers.celery import app
from newslyzer.workers.workflow import workflow

def parse_request():
    parser = reqparse.RequestParser()
    parser.add_argument('url', required=True)
    parser.add_argument('engine', type=str)
    return parser.parse_args()

class ArticleResource(Resource):
    def __init__(self):
        self.cache_service = CacheService()

    def get(self):
        start_api = timer()

        # params
        args = parse_request()
        url = args.get('url')

        cache = self.cache_service.get(url)

        if cache: # Cache hit returns cache
            return JSON(response=cache)
        else:
            print("Cache miss for URL {}. Genarating analysis.".format(url))

        result = workflow(url, app).get()

        self.cache_service.store(url, result)

        response = JSON(response=result)

        end_api = timer()
        print(">> Api: ", end_api - start_api)

        return response



def setup_app():
    flask = Flask(__name__)
    flask.debug = True

    api = Api(flask)
    api.add_resource(ArticleResource, '/article')

    CORS(app=flask, supports_credentials=True)
    return flask


if __name__ == '__main__':
    flask = setup_app()
    flask.run(threaded=True, host="0.0.0.0", use_reloader=True)
