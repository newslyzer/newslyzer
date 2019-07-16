from newslyzer.tasks import Task

metadata_keys = [ 'title', 'image', 'language', 'description', 'summary', 'url', 'sourceName', 'sourceUrl']
sentence_keys = [ 'id', 'text', 'sentiment' ]

class CreateView(Task):
    name = 'Process Sentences'
    provides = 'create-view'
    depends = [ 'process-sentences' ]

    def run(self, sentences, data):
        result = {
            'metadata': { key: data[key] for key in metadata_keys },
            'sentences': [],
            'people': [],
            'places': [],
            'organizations': [],
            'other': []
        }

        sentences_dict = {}
        entities_dict = {}

        for sentence in sentences:
            sentences_dict[sentence['id']] = sentence
            value = { key: sentence[key] for key in sentence_keys }
            result['sentences'].append(value)

            for entity in sentence['ner']:
                if not (entity['type'], entity['text']) in entities_dict:
                    entities_dict[(entity['type'], entity['text'])] = []
                entities_dict[(entity['type'], entity['text'])].append(sentence['id'])


        def append_entity(type, entity):
            if type == 'PER':
                result['people'].append(entity)
            elif type == 'LOC':
                result['places'].append(entity)
            elif type == 'ORG':
                result['organizations'].append(entity)
            else:
                result['other'].append(entity)

        for (type, name), sentences_ids in entities_dict.items():
            entity_sentences = [ sentences_dict[sid] for sid in sentences_ids ]
            sentiment = sum([ s['sentiment'] for s in entity_sentences ]) / len(entity_sentences)

            append_entity(type, {
                'name': name,
                'frequency': len(entity_sentences),
                'sentiment': sentiment,
                'context': [ { key: sentence[key] for key in sentence_keys } for sentence in entity_sentences ]
            })

        return result
