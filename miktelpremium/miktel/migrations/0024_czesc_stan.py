# Generated by Django 2.2.5 on 2019-09-22 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0023_auto_20190922_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='czesc',
            name='stan',
            field=models.IntegerField(choices=[(0, 'Nowy'), (1, 'Używany'), (2, 'Zamiennik'), (2, 'Z demontażu')], default=0, verbose_name='Stan czesci'),
        ),
    ]
