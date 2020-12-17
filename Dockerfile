FROM python:2.7

COPY requirements.txt /opt/app/
COPY eventpoi /opt/app/

WORKDIR /opt/app

RUN pip install -r /opt/app/requirements.txt

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
