# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#CMD gunicorn -w 4 -b 127.0.0.1:4000 app
#CMD gunicorn app:application --preload -b 0.0.0.0:5000
CMD exec gunicorn --workers 1 --threads 8 --timeout 0 app:app