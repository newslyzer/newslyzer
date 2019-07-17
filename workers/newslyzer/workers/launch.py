import gevent.monkey
gevent.monkey.patch_all()

import sys
import json
from time import sleep

from .workflow import workflow, run_one

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        # result = workflow(url, app).get()
        # print(json.dumps(result))

        res = workflow(url).then(
            lambda result: print(result.result))

        sleep(5)
        print('DONE')

    elif len(sys.argv) == 3:
        task = sys.argv[1]
        result = run_one(app, task, json.loads(sys.argv[2]))
        print(json.dumps(result.get()))

    else:
        raise('Incorrect number of arguments')
