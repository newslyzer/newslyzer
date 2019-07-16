from abc import ABC, abstractmethod
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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
            # print('task {} args: {}, kwargs: {}'.format(cls.provides, args, kwargs))
            logger.info('task {} args: {}, kwargs: {}'.format(cls.provides, args, kwargs))
            task_instance = cls(config, kwargs['context'])
            result = task_instance.run(*args)
            # print('task {} result: {}'.format(cls.provides, result))
            return result
        task


from .create_view import CreateView
from .download_article import DownloadArticle
from .join_analysis import JoinAnalysis
from .process_sentences import ProcessSentences
from .sentence import Sentence
from .sentiment_analysis import SentimentAnalysis

from .ner.flair_ner import FlairNER
from .ner.spacy_ner import SpacyNER
