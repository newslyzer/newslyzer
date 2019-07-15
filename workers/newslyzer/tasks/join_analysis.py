from newslyzer.tasks import Task

class JoinAnalysis(Task):
    name = 'Join Analysis'
    provides = 'join-analysis'
    depends = [ 'sentiment-analysis', 'named-entity-analysis' ]

    def run(self, results, sentence):
        return {
            'sentence': sentence,
            'sa_analysis': results[0],
            'ner_analysis': results[1]
        }

