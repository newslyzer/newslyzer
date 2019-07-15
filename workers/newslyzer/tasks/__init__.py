
from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, config, context):
        self.config = config
        self.context = context

    @abstractmethod
    def run(self, *args):
        pass

    @classmethod
    def register_task(cls, celery_app, config):
        @celery_app.task(name=cls.provides)
        def task(*args, **kwargs):
            print('task {} args: {}, kwargs: {}'.format(cls.provides, args, kwargs))
            task_instance = cls(config, kwargs['context'])
            return task_instance.run(*args)
        task


from .create_view import CreateView
from .download_article import DownloadArticle
from .join_analysis import JoinAnalysis
from .named_entity_analysis import NamedEntityAnalysis
from .process_sentences import ProcessSentences
from .sentence import Sentence
from .sentiment_analysis import SentimentAnalysis
