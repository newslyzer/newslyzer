from newslyzer.tasks import Task

class SentimentAnalysis(Task):
    # depends = [ 'clean-text' ]
    name = 'Sentiment Analysis'
    provides = 'sentiment-analysis'
    depends = [ 'sentence' ]

    def run(self, sentence):
        print('>> SentimentAnalysis {}'.format(sentence))
        return 0.0
