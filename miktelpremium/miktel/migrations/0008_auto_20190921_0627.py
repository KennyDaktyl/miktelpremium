# Generated by Django 2.2.5 on 2019-09-21 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0007_telefon_prcownik_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telefon',
            name='prcownik_out',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprzedajacy', to=settings.AUTH_USER_MODEL),
        ),
    ]
