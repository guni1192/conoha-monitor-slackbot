FROM python:3.6.5-alpine

RUN mkdir /app
WORKDIR /app

RUN pip install pipenv
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock

RUN pipenv install

ADD . /app

CMD pipenv run python app.py
