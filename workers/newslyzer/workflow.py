from celery import group, chord, signature, chain
import newslyzer.tasks as t

def workflow(url, app):
    context = {
        'sentiment_analysis': {
            'engine': 'engine1'
        },
    }

    def s(task):
        return app.signature(task, kwargs={ 'context': context })

    def ss(task, sentence):
        return app.signature(task, args=(sentence, ), kwargs={ 'context': context })

    print('workflow => {}'.format(url))
    prepare_data = chain(
        s('download-task'),
        # signature('parse-html'),
        # signature('clean-text'),
        s('process-sentences'),
    ).delay(url)

    sentences =  [
        group(
            ss('sentiment-analysis', sentence),
            ss('named-entity-analysis', sentence)
        ) | ss('join-analysis', sentence)
        for sentence in prepare_data.get()
    ]

    result_workflow = group(sentences) | s('create-view')


    return result_workflow.apply_async().get()
    # result = result.appy_async().get()
    # print('RESULT: {}'.format(result))
    # return result
    #return rest

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
