from celery import group, chord, signature, chain
import newslyzer.tasks as t

def run_one(app, task, *arguments):
    sig = app.signature(task, args=arguments, kwargs={ 'context': {} })
    return sig.apply_async().get()

def workflow(url, app):
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

    result = result_workflow.delay(data)

    return result.get()

def register_tasks(app, config):
    for task in [
        t.DownloadArticle,
        t.ProcessSentences,
        t.Sentence,
        t.SentimentAnalysis,
        t.NamedEntityAnalysis,
        t.JoinAnalysis,
        t.CreateView
    ]:
        print('Registering task: {}'.format(task.name))
        task.register_task(app, config)
