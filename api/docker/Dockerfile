FROM python:3.7-stretch

#RUN addgroup --gid 101 --system uwsgi
RUN adduser --system --disabled-login -uid 101 --shell /sbin/nologin --gid 101 uwsgi

# RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers uwsgi-python3
# RUN pip install cython

RUN pip install uwsgi

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY docker/uwsgi.ini /etc/uwsgi/

COPY newslyzer /newslyzer

RUN chown -R uwsgi /newslyzer

EXPOSE 5000

COPY docker/start.sh /

USER uwsgi

CMD /start.sh
