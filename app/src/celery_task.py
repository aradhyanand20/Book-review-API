from celery import Celery
from
c_app = Celery()
c_app.config_from_object('src.config')

def send_email():
