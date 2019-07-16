from newslyzer.tasks import Task
import nltk

class ProcessSentences(Task):
    # depends = [ 'clean-text' ]
    name = 'Process Sentences'
    provides = 'process-sentences'
    depends = [ 'download-article' ]

    def run(self, data):
        text = data.pop('text', '')

        data['sentences'] = []
        current_id = 0

        for sentence in nltk.tokenize.sent_tokenize(text):
            data['sentences'].append({
                'id': current_id,
                'text': sentence
            })

            current_id += 1

        return data
