FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "--app", "app", "--debug", "run"]