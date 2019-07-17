from celery import group, chord, signature, chain

from .celery import app

def run_one(task, *arguments):
    sig = app.signature(task, args=arguments, kwargs={ 'context': {} })
    return sig.delay()

def workflow2():
    def s(task, *args):
        return app.signature(task, args=args, kwargs={ 'context': {} })

    return s('download-article')
    # return chain(
    #     s('download-article'),
    #     # signature('parse-html'),
    #     # signature('clean-text'),
    #     s('process-sentences'),
    # )

def workflow(url):
    context = {
        'sentiment_analysis': {
            'engine': 'engine1'
        },
    }

    def s(task, *args):
        return app.signature(task, args=args, kwargs={ 'context': context })

    def ss(task, sentence):
        return app.signature(task, args=(sentence, ), kwargs={ 'context': context })

    print('workflow => {}'.format(url))
    prepare_data = chain(
        s('download-article'),
        # signature('parse-html'),
        # signature('clean-text'),
        s('process-sentences'),
    ).delay(url)

    data = prepare_data.get()

    sentences =  [
        group(
            ss('sentiment-analysis', sentence),
            ss('named-entity-analysis', sentence)
        ) | ss('join-analysis', sentence)
        for sentence in data['sentences']
    ]

    result_workflow = group(sentences) | s('create-view', data)

    return result_workflow.delay(data)

