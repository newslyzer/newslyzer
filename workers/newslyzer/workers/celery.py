from celery import Celery

from .config import redis_connection
from .tasks import *

def register_tasks(app, config):
    for task in [
        DownloadArticle,
        ProcessSentences,
        Sentence,
        SentimentAnalysis,
        # FlairNER,
        SpacyNER,
        JoinAnalysis,
        CreateView
    ]:
        print('Registering task: {}'.format(task.name))
        task.register_task(app, config)

app = Celery(broker=redis_connection, backend=redis_connection)

app.conf.task_routes = {
    'named-entity-analysis': { 'queue': 'ner' }
}

config = {}

register_tasks(app, config)
