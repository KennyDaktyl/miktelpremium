# Generated by Django 2.2.5 on 2019-09-21 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0010_telefon_sklep_sprzed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefon',
            name='pracownik_out',
        ),
    ]
