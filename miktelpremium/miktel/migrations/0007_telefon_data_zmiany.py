# Generated by Django 2.2.6 on 2019-10-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0006_auto_20191028_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='telefon',
            name='data_zmiany',
            field=models.DateField(blank=True, null=True),
        ),
    ]