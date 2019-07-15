from newslyzer.tasks import Task
import nltk

class ProcessSentences(Task):
    # depends = [ 'clean-text' ]
    name = 'Process Sentences'
    provides = 'process-sentences'
    depends = [ 'download-task' ]

    def run(self, text):
        return nltk.tokenize.sent_tokenize(text)
