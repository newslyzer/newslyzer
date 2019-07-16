source /home/alotor/.virtualenvs/newslyzer/bin/activate

PYTHONPATH=$(pwd)/workers python -m newslyzer.workers.launch $*
