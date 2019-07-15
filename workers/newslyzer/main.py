from celery import Celery
from .workflow import register_tasks

app = Celery(
    'main',
    broker='pyamqp://guest@127.0.0.1//',
    backend='redis://127.0.0.1'
)

config = {}

register_tasks(app, config)
