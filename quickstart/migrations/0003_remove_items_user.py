# Generated by Django 3.2 on 2021-06-03 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_items_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='user',
        ),
    ]
