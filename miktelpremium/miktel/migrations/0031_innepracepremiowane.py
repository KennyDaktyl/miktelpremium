# Generated by Django 2.2.5 on 2019-09-24 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0030_auto_20190924_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='InnePracePremiowane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=128, verbose_name='Nazwa czynności premiowanej')),
                ('czas', models.IntegerField(verbose_name='Czas trwania w godzinach lub ilość')),
                ('opis', models.TextField(blank=True, null=True, verbose_name='Opis wykonanje czynności')),
                ('data', models.DateField(auto_now_add=True, verbose_name='Data')),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
