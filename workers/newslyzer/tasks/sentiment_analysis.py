from newslyzer.tasks import Task
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalysis(Task):
    # depends = [ 'clean-text' ]
    name = 'Sentiment Analysis'
    provides = 'sentiment-analysis'
    depends = [ 'sentence' ]

    def run(self, sentence):
        if not 'sid' in self.context:
            self.context['sid'] = SentimentIntensityAnalyzer()

        ss = self.context['sid'].polarity_scores(sentence)
        return ss['compound']
