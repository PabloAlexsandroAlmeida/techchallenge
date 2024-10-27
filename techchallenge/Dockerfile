FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    python3-setuptools \
    python3-dev \
    build-essential \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    && apt-get clean

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py dataset_stage-1
RUN python manage.py dataset_stage-2

ENV DJANGO_SETTINGS_MODULE=techchallenge.settings
ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "techchallenge.wsgi", "--master", "--processes", "4", "--threads", "2"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]