from newslyzer.tasks import Task

class JoinAnalysis(Task):
    name = 'Join Analysis'
    provides = 'join-analysis'
    depends = [ 'sentiment-analysis', 'named-entity-analysis' ]

    def run(self, results, sentence):
        result = {}

        for curr in results:
            result.update(curr)

        return result

