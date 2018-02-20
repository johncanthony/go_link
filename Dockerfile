FROM alpine:3.6

MAINTAINER John Anthony <jca310ms@gmail.com>

RUN apt-get update
RUN apt install -y python python-pip gnicorn python-virtualenv

#Flask App
RUN mkdir -p /deploy/app
COPY gunicorn_conf.py /deploy/gunicorn_conf.py
COPY app /deploy/app
RUN pip install -r /deploy/run/requirements.txt

WORKDIR /deploy/app

EXPOSE 8081

CMD ["/usr/bin/gunicorn","--config", "/deploy/gunicorn_conf.py", "app:app"]
