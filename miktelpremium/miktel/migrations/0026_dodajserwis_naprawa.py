# Generated by Django 2.2.5 on 2019-09-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0025_auto_20190922_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='dodajserwis',
            name='naprawa',
            field=models.BooleanField(default=True),
        ),
    ]
