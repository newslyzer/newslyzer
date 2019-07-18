source /home/alotor/.virtualenvs/newslyzer/bin/activate

PYTHONPATH=$(pwd)/workers celery worker -n worker1 -A newslyzer.workers.celery -Q celery --concurrency=10 $* &
PYTHONPATH=$(pwd)/workers celery worker -n worker2 -A newslyzer.workers.celery -Q ner --concurrency=2 $*
