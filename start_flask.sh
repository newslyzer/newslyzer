source /home/alotor/.virtualenvs/newslyzer/bin/activate

PYTHONPATH=$(pwd)/workers:$(pwd)/api python -m newslyzer.api.server
