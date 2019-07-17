from celery import Celery, group, signature, chain

celery = Celery(
    broker='redis://127.0.0.1',
    backend='redis://127.0.0.1'
)

celery.conf.task_routes = {
    'named-entity-analysis': { 'queue': 'ner' }
}

def start_worker(url):
    context = {
        'sentiment_analysis': {
            'engine': 'engine1'
        },
    }

    def s(task, *args):
        return celery.signature(task, args=args, kwargs={ 'context': context })

    def ss(task, *args):
        return celery.signature(task, args=args, kwargs={ 'context': context })

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
        ) | ss('join-analysis', sentence, data['url'], 100 / len(data['sentences']))
        for (i, sentence) in enumerate(data['sentences'])
    ]

    result_workflow = group(sentences) | s('create-view', data)

    return result_workflow.delay(data)

