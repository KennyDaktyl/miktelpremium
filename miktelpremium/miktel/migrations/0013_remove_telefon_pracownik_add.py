# Generated by Django 2.2.5 on 2019-09-21 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0012_telefon_pracownik_add'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefon',
            name='pracownik_add',
        ),
    ]
