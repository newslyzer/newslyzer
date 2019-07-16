from . import Task

from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalysis(Task):
    # depends = [ 'clean-text' ]
    name = 'Sentiment Analysis'
    provides = 'sentiment-analysis'
    depends = [ 'sentence' ]

    def run(self, data, sentence):
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence['text'])
        sentence['sentiment'] = ss['compound']
        return sentence
