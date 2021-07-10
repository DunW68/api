# Create your tasks here
import random
import string

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from djangoProject.settings import EMAIL_HOST_USER
from quickstart.models import Items
from djangoProject.celery import app
from rest_framework.authtoken.models import Token

@app.task()
#@shared_task
def create_new_item():
    random_name = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
    new_item = Items.objects.create(name=random_name, description='asd', price=111)
    return new_item.name

@app.task()
def send_ok_email(mail):
     send_mail(
        'Cart description',
        'It`s ok!',
        EMAIL_HOST_USER,
        [mail],
        fail_silently=False,
    )