# Generated by Django 2.2.5 on 2019-09-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0031_innepracepremiowane'),
    ]

    operations = [
        migrations.AddField(
            model_name='usluga',
            name='akcesoria',
            field=models.BooleanField(default=False),
        ),
    ]
