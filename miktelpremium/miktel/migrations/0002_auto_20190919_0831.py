# Generated by Django 2.2.5 on 2019-09-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fakturazakupu',
            name='telefon',
        ),
        migrations.AddField(
            model_name='telefon',
            name='faktura',
            field=models.ManyToManyField(to='miktel.FakturaZakupu'),
        ),
    ]
