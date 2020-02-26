FROM python:3.8

RUN pip install pipenv
RUN pipenv install

EXPOSE 27017