from . import Task

from newslyzer.workers.config import redis_host, redis_port

from redis import Redis

class JoinAnalysis(Task):
    name = 'Join Analysis'
    provides = 'join-analysis'
    depends = [ 'sentiment-analysis', 'named-entity-analysis' ]

    def run(self, results, sentence, url, offset):
        result = {}

        for curr in results:
            result.update(curr)

        redis = Redis(host=redis_host, port=int(redis_port))
        counter = redis.incr('url:{}:completed'.format(url))
        progress = counter * offset
        redis.publish('url:{}:progress'.format(url), progress)

        return result

