# Generated by Django 3.0.3 on 2020-03-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0002_auto_20200315_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telefon',
            name='slug',
            field=models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug'),
        ),
    ]
