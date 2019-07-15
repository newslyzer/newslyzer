from newslyzer.tasks import Task

class Sentence(Task):
    name = 'Sentence'
    provides = 'sentence'
    depends = []

    def run(self, sentence):
        print('>> Sentence {}'.format(sentence))
        return sentence
