# Generated by Django 2.2.5 on 2019-09-26 05:25

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status_osoby', models.IntegerField(blank=True, choices=[(0, 'Właścicel'), (1, 'Pracownik'), (2, 'Osoba zewnętrzna')], null=True, verbose_name='Status w Firmie')),
                ('umowa', models.IntegerField(blank=True, choices=[(0, 'Umowa o prace'), (1, 'Umowa zlecenie'), (2, 'Brak danych')], null=True, verbose_name='Rodzaj zatrudnienia')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Info')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Adres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ulica', models.CharField(max_length=128, verbose_name='Ulica')),
                ('miasto', models.CharField(max_length=128, verbose_name='Miasto')),
                ('kod', models.CharField(max_length=128, verbose_name='Kod pocztowy')),
                ('numerTelefonu', models.CharField(max_length=128, verbose_name='Numer telefonu')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='images/')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('alt', models.CharField(blank=True, max_length=128, null=True)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Hurtownia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Marka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Sklep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64, verbose_name='Nazwa')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Foto')),
                ('adres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Adres')),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Telefon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stan', models.IntegerField(choices=[(0, 'Nowy'), (1, 'Używany'), (2, 'Bez pudełka')], verbose_name='Stan telefon')),
                ('nazwa', models.CharField(max_length=64, verbose_name='Model')),
                ('imei', models.CharField(max_length=14, verbose_name='imei')),
                ('cena_zak', models.FloatField()),
                ('cena_sprzed', models.IntegerField(blank=True, null=True)),
                ('dostepny', models.BooleanField(default=True)),
                ('dokument', models.BooleanField(default=False)),
                ('kategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Kategoria')),
                ('marka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('pracownik_sprzed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprzdawal', to=settings.AUTH_USER_MODEL)),
                ('pracownik_zak', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='przyjmowal', to=settings.AUTH_USER_MODEL)),
                ('sklep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('sklep_sprzed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sklep_sprzadzy', to='miktel.Sklep')),
            ],
            options={
                'ordering': ('marka', 'nazwa'),
            },
        ),
        migrations.CreateModel(
            name='Typ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Usluga',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=64)),
                ('typ', models.IntegerField(choices=[(0, 'Procent'), (1, 'cena/szt')], default=0, verbose_name='Typ prowizji')),
                ('kwota', models.IntegerField(default=0)),
                ('czesci', models.BooleanField(default=False)),
                ('zakup', models.BooleanField(default=False)),
                ('sprzedaz', models.BooleanField(default=False)),
                ('grawer', models.BooleanField(default=False)),
                ('akcesoria', models.BooleanField(default=False)),
                ('sklep', models.ManyToManyField(to='miktel.Sklep')),
            ],
            options={
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='UmowaKomisowaNew',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(blank=True, max_length=64, null=True, verbose_name='Numer umowa')),
                ('komitent', models.CharField(max_length=128, verbose_name='Dane komitenta')),
                ('adres_komitenta', models.CharField(max_length=128, verbose_name='Adres komitenta')),
                ('numer_dowodu', models.CharField(max_length=9, verbose_name='Numer dowodu')),
                ('data_zak', models.DateTimeField(auto_now_add=True)),
                ('sprzedana', models.BooleanField(default=False)),
                ('data_sprzed', models.DateTimeField(blank=True, null=True)),
                ('phones', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Telefon')),
                ('pracownik_sprzed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pracownik_sprzedaż', to=settings.AUTH_USER_MODEL)),
                ('pracownik_zak', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pracownik_kupujący', to=settings.AUTH_USER_MODEL)),
                ('sklep_zak', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep', verbose_name='Miejsce zakupu')),
            ],
        ),
        migrations.CreateModel(
            name='PremiaJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.IntegerField(default=0)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('cena_klient', models.IntegerField(blank=True, default=0, null=True, verbose_name='Cena klient')),
                ('koszt', models.IntegerField(blank=True, default=0, null=True, verbose_name='Koszty')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sklep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('usluga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Usluga')),
            ],
        ),
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
        migrations.CreateModel(
            name='FakturaZakupu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer', models.CharField(max_length=64)),
                ('data_zak', models.DateField(auto_now_add=True)),
                ('hurtownia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Hurtownia')),
                ('pracownik_zak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sklep', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('telefon', models.ManyToManyField(to='miktel.Telefon')),
            ],
        ),
        migrations.CreateModel(
            name='DodajSerwis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('imei', models.CharField(blank=True, max_length=14, null=True)),
                ('cena_zgoda', models.IntegerField(blank=True, default=0, null=True, verbose_name='Cena naprawy')),
                ('koszt', models.IntegerField(blank=True, default=0, null=True, verbose_name='Koszty')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('data_wydania', models.DateTimeField(blank=True, null=True)),
                ('numer_telefonu', models.CharField(blank=True, max_length=15, null=True)),
                ('imie_nazwisko', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Przyjęty na seriws'), (2, 'W naprawie'), (3, 'Oczekuje na decyzję klienta'), (4, 'Gotowy do odbioru'), (5, 'Wydany'), (6, 'Poprawka'), (7, 'Reklamacja')], default=1, verbose_name='Status naprawy')),
                ('info', models.CharField(blank=True, max_length=256, null=True)),
                ('archiwum', models.BooleanField(default=False)),
                ('naprawa', models.BooleanField(default=True)),
                ('marka', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka', verbose_name='Wybierz marke')),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Przyjmujacy', to=settings.AUTH_USER_MODEL)),
                ('serwisant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Naprawiajacy', to=settings.AUTH_USER_MODEL)),
                ('sklep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('usluga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Usluga')),
            ],
        ),
        migrations.CreateModel(
            name='Czesc',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=64)),
                ('stan', models.IntegerField(choices=[(0, 'Nowy'), (1, 'Używany'), (2, 'Zamiennik'), (3, 'Z demontażu')], default=0, verbose_name='Stan czesci')),
                ('kolor', models.IntegerField(choices=[(0, 'Czarny'), (1, 'Biały'), (2, 'Złoty'), (3, 'Niebieski'), (4, 'Inny')], default=0, verbose_name='Kolor czesci')),
                ('date_add', models.DateField(auto_now_add=True)),
                ('cena_zak', models.IntegerField()),
                ('cena_sprzed', models.IntegerField(blank=True, null=True)),
                ('ilosc', models.IntegerField()),
                ('opis', models.CharField(blank=True, max_length=128, null=True)),
                ('dostepny', models.BooleanField(default=True)),
                ('foto', models.ManyToManyField(blank=True, to='miktel.Foto', verbose_name='Foto_produktu')),
                ('marka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('pracownik', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Wprowadził')),
                ('sklep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep', verbose_name='Magazyn')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Typ')),
            ],
            options={
                'ordering': ('marka', 'typ', 'nazwa'),
            },
        ),
        migrations.AddField(
            model_name='myuser',
            name='adres',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Adres'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='foto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Foto'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sklep',
            field=models.ManyToManyField(related_name='Miejsce_pracy', to='miktel.Sklep'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sklep_dzisiaj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
