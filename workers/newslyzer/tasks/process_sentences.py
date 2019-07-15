from newslyzer.tasks import Task

class ProcessSentences(Task):
    # depends = [ 'clean-text' ]
    name = 'Process Sentences'
    provides = 'process-sentences'
    depends = [ 'download-task' ]

    def run(self, text):
        print('>> ProcessSentences {}'.format(text))
        lines = [line.lstrip() for line in text.split('\n')]
        return lines
        # header = [ sentence_workflow(line) for line in lines ]
        # return group(header).apply_async().get()
