# Generated by Django 3.0.3 on 2020-11-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='site_id',
            field=models.IntegerField(blank=True, choices=[(2, 'GSM'), (5, 'Klucze'), (1, 'Home'), (4, 'Pieczątki'), (3, 'Grawerowanie')], null=True, verbose_name='Strona'),
        ),
    ]
