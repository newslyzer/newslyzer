from .workflow import workflow
from .main import app

# job = app.signature('download-task', ('https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html',))
url = 'https://www.eldiario.es/politica/Sanchez-Iglesias-convocar-consulta-maximalista_0_920757950.html'

result = workflow(url, app)

print(result)
