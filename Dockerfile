FROM ubuntu:18.04

MAINTAINER John Anthony <jca310ms@gmail.com>

RUN apt-get update
RUN apt-get install -y python python-pip python-virtualenv gunicorn 

#Flask App
RUN mkdir -p /deploy/app
COPY app /deploy/app
RUN pip install -r /deploy/app/requirements.txt

WORKDIR /deploy/app

EXPOSE 8081

CMD ["gunicorn","--bind","0.0.0.0:8081","app:app"]
