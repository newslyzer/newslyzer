from .. import Task

from flair.data import Sentence
from flair.models import SequenceTagger

class FlairNER(Task):
    # depends = [ 'clean-text' ]
    name = 'Named Entity Analysis (FLAIR)'
    provides = 'named-entity-analysis'
    depends = [ 'sentence' ]

    def run(self, data, sentence):
        if (not 'tagger' in self.config):
            self.config['tagger'] = SequenceTagger.load('ner-multi-fast')

        sent_model = Sentence(sentence['text'])
        self.config['tagger'].predict(sent_model)

        sentence['ner'] = [ {
            'text': d['text'],
            'type': d['type']
        } for d in [ span.to_dict() for span in sent_model.get_spans('ner') ]]

        return sentence
