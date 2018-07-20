# sw_web_app
[![CircleCI](https://circleci.com/gh/eskemojoe007/sw_web_app.svg?style=shield)](https://circleci.com/gh/eskemojoe007/sw_web_app)

## Background
This project is a `django` project designed to search, save and get southwest flights.

## Installation in local mode
I use `pipenv` for everything.  To install follow these steps:

1. Install python 3-64 bit.
2. Install pipenv globablly `pip install pipenv`
3. Clone this repository
4. In the repository run `pipenv install --dev`

### Launching the server
run `pipenv run python manage.py runserver`

### Running all the tests
run `pipenv run python -m pytest`

## Celery Installs and notes
As I play with celery, I wanted to document everything I've been doing
to install celery locally for testing.  Then we'll install and deploy Celery
later

http://www.rabbitmq.com/install-windows.html
1. Install Erlang 21.x with admin mode
2. Install Rabbitmq installer

Then for the project I install celery pipenv install celery

I also used the rabbitmq command line to set the following settings:
http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html#setting-up-rabbitmq

In windows I had to add `set FORKED_BY_MULTIPROCESSING=1`.  See https://github.com/celery/celery/pull/4078 and https://github.com/celery/celery/issues/4178
