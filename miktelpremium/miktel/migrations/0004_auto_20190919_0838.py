# Generated by Django 2.2.5 on 2019-09-19 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0003_auto_20190919_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefon',
            name='faktura',
        ),
        migrations.AddField(
            model_name='fakturazakupu',
            name='telefon',
            field=models.ManyToManyField(to='miktel.Telefon'),
        ),
    ]
