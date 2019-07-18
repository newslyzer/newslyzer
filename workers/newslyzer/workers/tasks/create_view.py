from . import Task

import uuid
from os import path
from wordcloud import WordCloud
from newslyzer.workers.config import word_cloud_path

def get_sentiment_color(sentiment):
    very_negative = (238, 90, 90)
    negative = (255, 177, 116)
    neutral = (252, 227, 138)
    positive = (143, 236, 200)
    very_positive = (29, 205, 159)

    if sentiment < -0.6:
        return very_negative
    elif sentiment < -0.2:
        return negative
    elif sentiment < 0.2:
        return neutral
    elif sentiment < 0.6:
        return positive
    else:
        return very_positive


def generate_word_cloud(url, freq_word_dict, sent_word_dict):
    def get_word_color(word, **kwargs):
        return get_sentiment_color(sent_word_dict[word])

    cloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        color_func=get_word_color)

    tags = cloud.generate_from_frequencies(freq_word_dict)
    image = tags.to_image()
    image_file = str(uuid.uuid4()) + '.png'
    image.save(path.join(word_cloud_path, image_file), format='png', optimized=True)
    return image_file


metadata_keys = [ 'title', 'image', 'language', 'description', 'summary', 'url', 'sourceName', 'sourceUrl']
sentence_keys = [ 'id', 'text', 'sentiment' ]

class CreateView(Task):
    name = 'Process Sentences'
    provides = 'create-view'
    depends = [ 'process-sentences' ]

    def run(self, sentences, data):
        result = {
            'status': 'processed',
            'metadata': { key: data[key] for key in metadata_keys },
            'sentences': [],
            'people': [],
            'places': [],
            'organizations': [],
            'other': []
        }

        sentences_dict = {}
        entities_dict = {}
        sum_sentiment = 0

        for sentence in sentences:
            sentences_dict[sentence['id']] = sentence
            value = { key: sentence[key] for key in sentence_keys }
            result['sentences'].append(value)
            sum_sentiment += sentence['sentiment']

            for entity in sentence['ner']:
                if not (entity['type'], entity['text']) in entities_dict:
                    entities_dict[(entity['type'], entity['text'])] = []
                entities_dict[(entity['type'], entity['text'])].append(sentence['id'])

        result['metadata']['sentiment'] = sum_sentiment / len(sentences)

        freq_words_dict = {}
        sent_words_dict = {}
        def append_entity(type, entity):
            if type == 'PER':
                result['people'].append(entity)
            elif type == 'LOC':
                result['places'].append(entity)
            elif type == 'ORG':
                result['organizations'].append(entity)
            else:
                result['other'].append(entity)

            freq_words_dict[entity['name']] = entity['frequency']
            sent_words_dict[entity['name']] = entity['sentiment']

        for (type, name), sentences_ids in entities_dict.items():
            entity_sentences = [ sentences_dict[sid] for sid in sentences_ids ]
            sentiment = sum([ s['sentiment'] for s in entity_sentences ]) / len(entity_sentences)

            append_entity(type, {
                'name': name,
                'frequency': len(entity_sentences),
                'sentiment': sentiment,
                'context': [ { 'sentence': sentence['text'], 'sentiment': sentence['sentiment'] } for sentence in entity_sentences ]
            })

        result['wordcloud'] = generate_word_cloud(data['url'], freq_words_dict, sent_words_dict)
        return result
