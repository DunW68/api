# Generated by Django 3.2.3 on 2021-06-03 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_remove_items_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='description',
            field=models.TextField(default=None, max_length=299),
            preserve_default=False,
        ),
    ]