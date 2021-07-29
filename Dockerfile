FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY /api/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/