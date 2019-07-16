source /home/alotor/.virtualenvs/newslyzer/bin/activate

PYTHONPATH=$(pwd)/workers celery worker -n worker1 -A newslyzer.workers.celery -Q celery,ner --concurrency=10
