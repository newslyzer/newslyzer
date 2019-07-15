from newslyzer.tasks import Task

class CreateView(Task):
    name = 'Process Sentences'
    provides = 'create-view'
    depends = [ 'process-sentences' ]

    def run(self, result):
        print('>> CreateView {}'.format(result))
        return result
