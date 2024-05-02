FROM python:3.10

RUN mkdir usr/app

WORKDIR usr/app

COPY "app.py" .
COPY "db.py" .
COPY "requirements.txt" .

RUN pip3 install -r requirements.txt

CMD python3 app.py 
