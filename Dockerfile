FROM python:3.10.12

WORKDIR /code

COPY . /code

RUN pip install --no-cache --upgrade -r requirements.txt
