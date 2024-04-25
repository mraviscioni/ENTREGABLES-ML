FROM python:3.11.0-alpine3.16

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]