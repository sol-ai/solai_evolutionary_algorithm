FROM python:3.8
ADD . /solai_evolutionary_algorithm
WORKDIR /solai_evolutionary_algorithm
RUN pip install -r requirements.txt

EXPOSE 27017