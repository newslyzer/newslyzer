from celery import Celery
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

app = Celery(
    'main',
    broker='pyamqp://guest@127.0.0.1//',
    backend='redis://127.0.0.1'
)

app.conf.task_routes = {
    'named-entity-analysis': { 'queue': 'ner' }
}

config = {}

register_tasks(app, config)
