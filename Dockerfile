# pull official base image
#FROM python:3.8-slim-buster
FROM jjanzic/docker-python3-opencv

# set work directory
WORKDIR /usr/src/app

# set environment variable
ENV PYTHONDONTWRTIEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . /usr/src/app/

# install dependencies
#RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD ["bash", "-c", "python manage.py migrate --run-syncdb && gunicorn smart_robot.wsgi:application  --bind 0.0.0.0:8000"]