# Generated by Django 3.0.3 on 2020-11-06 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0002_auto_20201104_1226'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='sklep',
        #     name='is_active',
        #     field=models.BooleanField(default=True),
        # ),
        migrations.AlterField(
            model_name='articles',
            name='site_id',
            field=models.IntegerField(blank=True, choices=[(2, 'GSM'), (5, 'Klucze'), (4, 'Pieczątki'), (3, 'Grawerowanie'), (1, 'Home')], null=True, verbose_name='Strona'),
        ),
    ]
