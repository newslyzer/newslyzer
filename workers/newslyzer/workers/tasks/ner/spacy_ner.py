from .. import Task

import spacy

class SpacyNER(Task):
    # depends = [ 'clean-text' ]
    name = 'Named Entity Analysis (FLAIR)'
    provides = 'named-entity-analysis'
    depends = [ 'sentence' ]

    def run(self, data, sentence):
        if (not 'model' in self.config):
            self.config['model'] = spacy.load('xx_ent_wiki_sm')

        nlp = self.config['model']
        tagged = nlp(sentence['text'])

        sentence['ner'] = [ {
            'text': e.text,
            'type': e.label_
        } for e in tagged.ents ]

        return sentence
