from . import Task

class Sentence(Task):
    name = 'Sentence'
    provides = 'sentence'
    depends = []

    def run(self, sentence):
        return sentence
