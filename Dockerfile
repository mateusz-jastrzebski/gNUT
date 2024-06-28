FROM python:3.12-alpine

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}
ENV PORT=${PORT:-8123}

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py createdefaultadmin && gunicorn --bind 0.0.0.0:$PORT webNUT.wsgi:application"]
