from newslyzer.tasks import Task

class NamedEntityAnalysis(Task):
    # depends = [ 'clean-text' ]
    name = 'Named Entity Analysis'
    provides = 'named-entity-analysis'
    depends = [ 'sentence' ]

    def run(self, sentence):
        print('>> NamedEntityAnalysis {}'.format(sentence))
        return { 'lorem': 'NP', 'ipsum': 'NPP' }
