# Generated by Django 2.2.5 on 2019-09-22 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0018_auto_20190922_0645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='premiajob',
            old_name='check_id',
            new_name='check',
        ),
    ]