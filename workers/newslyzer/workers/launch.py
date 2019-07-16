import sys
import json

from .workflow import workflow, run_one
from .celery import app

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        result = workflow(url, app).get()
        print(json.dumps(result))

    elif len(sys.argv) == 3:
        task = sys.argv[1]
        result = run_one(app, task, json.loads(sys.argv[2]))
        print(json.dumps(result.get()))

    else:
        raise('Incorrect number of arguments')
