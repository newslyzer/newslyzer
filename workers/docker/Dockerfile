FROM python:3.7-stretch

RUN adduser --system --disabled-login -uid 101 --shell /sbin/nologin --gid 101 newslyzer

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN python -m spacy download xx_ent_wiki_sm && \
    python -m spacy download es_core_news_sm && \
    python -m spacy download en_core_web_sm

USER newslyzer

RUN python -c "import nltk; nltk.download([ 'punkt', 'vader_lexicon' ])"

#RUN python -c "from flair.models import SequenceTagger; \
#    SequenceTagger.load('ner-multi'); \
#    SequenceTagger.load('ner-multi-fast')"


COPY newslyzer /newslyzer

CMD [ "sh", "-c", "celery worker -A newslyzer.workers.celery -Q celery,ner --concurrency=10 -l info"]
