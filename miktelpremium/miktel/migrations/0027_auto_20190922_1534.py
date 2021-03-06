# Generated by Django 2.2.5 on 2019-09-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miktel', '0026_dodajserwis_naprawa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dodajserwis',
            name='status',
            field=models.IntegerField(choices=[(1, 'Przyjęty na seriws'), (2, 'W naprawie'), (3, 'Oczekuje na decyzję klienta'), (4, 'Gotowy do odbioru'), (5, 'Wydany'), (6, 'Poprawka'), (7, 'Reklamacja')], default=1, verbose_name='Status naprawy'),
        ),
    ]
