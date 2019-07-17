source /home/alotor/.virtualenvs/newslyzer/bin/activate

PYTHONPATH=$(pwd)/api python -m newslyzer.api.server
