import sys
import json

from .workflow import workflow, run_one
from .main import app

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # job = app.signature('download-task', ('https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html',))
        url = 'https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html'
        result = workflow(url, app)
        print(result)

    elif len(sys.argv) == 3:
        task = sys.argv[1]
        result = run_one(app, task, json.loads(sys.argv[2]))
        print(json.dumps(result))

    else:
        raise('Incorrect number of arguments')
