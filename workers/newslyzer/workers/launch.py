import sys
import json

from .workflow import workflow, run_one
from .celery import app

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # job = app.signature('download-task', ('https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html',))
        # url = 'https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html'
        url = 'http://localhost:1111/Pedro%20S%C3%A1nchez%20sube%20el%20tono%20contra%20Iglesias%20para%20redoblar%20la%20presi%C3%B3n%20a%20las%20puertas%20de%20la%20investidura.html'
        result = workflow(url, app).get()
        print(json.dumps(result))

    elif len(sys.argv) == 3:
        task = sys.argv[1]
        result = run_one(app, task, json.loads(sys.argv[2]))
        print(json.dumps(result.get()))

    else:
        raise('Incorrect number of arguments')
