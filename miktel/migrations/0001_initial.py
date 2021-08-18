# Generated by Django 3.0.3 on 2020-11-04 11:26

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


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
                ('hour_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name_plural': 'Osoby w firmie',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Adres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ulica', models.CharField(max_length=32, verbose_name='Ulica')),
                ('miasto', models.CharField(max_length=32, verbose_name='Miasto')),
                ('ulica_slug', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ulica do URL')),
                ('miasto_slug', models.CharField(blank=True, max_length=32, null=True, verbose_name='Miasto do URL')),
                ('kod', models.CharField(max_length=10, verbose_name='Kod pocztowy')),
                ('numerTelefonu', models.CharField(max_length=10, verbose_name='Numer telefonu')),
                ('latitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='lititude')),
                ('longitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='longitude')),
                ('google_maps', models.TextField(blank=True, null=True, verbose_name='link do google maps')),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Adresy',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('name_slug', models.CharField(blank=True, max_length=64, null=True)),
                ('accessories', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Kategorie',
                'ordering': ('name',),
            },
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
                ('cena_promo', models.FloatField(blank=True, null=True)),
                ('in_promo', models.BooleanField(default=False)),
                ('ilosc', models.IntegerField()),
                ('opis', models.CharField(blank=True, max_length=128, null=True)),
                ('dostepny', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Czesci_gsm',
                'ordering': ('marka', 'nazwa'),
            },
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('slug', models.CharField(blank=True, max_length=64, null=True)),
                ('accessories', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Producent',
                'ordering': ('name',),
            },
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
                'verbose_name_plural': 'Nasi dostawcy',
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
                'verbose_name_plural': 'Kategorie telefonów GSM',
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Marka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64)),
                ('gsm', models.BooleanField(default=False)),
                ('keys', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Marka',
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Materiał',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
            ],
            options={
                'verbose_name_plural': 'Kategorie główne',
                'ordering': ('id', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Sklep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=64, verbose_name='Nazwa')),
                ('nazwa_slug', models.CharField(blank=True, max_length=64, null=True, verbose_name='Nazwa do URL')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Foto')),
                ('serwis_zew', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
                ('adres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Adres')),
            ],
            options={
                'verbose_name_plural': 'Nasze sklepy',
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='Telefon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stan', models.IntegerField(choices=[(0, 'Nowy'), (1, 'Używany'), (2, 'Bez pudełka')], verbose_name='Stan telefon')),
                ('nazwa', models.CharField(max_length=64, verbose_name='Model')),
                ('imei', models.CharField(max_length=15, verbose_name='imei')),
                ('cena_zak', models.FloatField()),
                ('cena_sprzed', models.FloatField(blank=True, null=True)),
                ('cena_promo', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('in_promo', models.BooleanField(default=False)),
                ('dostepny', models.BooleanField(default=True)),
                ('zawieszony', models.BooleanField(default=False)),
                ('dokument', models.BooleanField(default=False)),
                ('data_wprow', models.DateField(blank=True, null=True)),
                ('data_sprzed', models.DateField(blank=True, null=True)),
                ('data_zmiany', models.DateField(blank=True, null=True, verbose_name='Data zmiany (YYYY-MM-DD)')),
                ('nr_doc', models.CharField(blank=True, max_length=64, null=True, verbose_name='Nr dokumentu')),
                ('info', models.CharField(blank=True, max_length=256, null=True, verbose_name='Informacje')),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Nazwa slug')),
                ('foto', models.ManyToManyField(blank=True, to='miktel.Foto')),
                ('kategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Kategoria')),
                ('magazyn_aktualny', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Sklep_aktualny', to='miktel.Sklep', verbose_name='Aktualnie dostępny w:')),
                ('marka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('pracownik_sprzed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprzdawal', to=settings.AUTH_USER_MODEL)),
                ('pracownik_zak', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='przyjmowal', to=settings.AUTH_USER_MODEL)),
                ('sklep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('sklep_sprzed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sklep_sprzadzy', to='miktel.Sklep')),
            ],
            options={
                'verbose_name_plural': 'Telefony',
                'ordering': ('-id', 'marka', 'nazwa', 'kategoria'),
            },
        ),
        migrations.CreateModel(
            name='Typ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Typ czesci',
                'ordering': ('nazwa',),
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('time_start', models.TimeField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('time_duration', models.TimeField(blank=True, null=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep', verbose_name='Magazyn')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Grafik',
                'ordering': ('-date', '-time_duration'),
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
                'verbose_name_plural': 'Usługi nazwa',
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
            options={
                'verbose_name_plural': 'Umowy komisowe',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('price_promo', models.FloatField(blank=True, null=True)),
                ('is_promo', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_new', models.BooleanField(default=False)),
                ('info', models.TextField(blank=True, null=True)),
                ('sale', models.IntegerField(choices=[(0, 'Nie'), (1, 'Sale -10%'), (2, 'Sale -20%'), (3, 'Sale -30%'), (4, 'Sale -40%'), (5, 'Sale -50%'), (6, 'All 5 zł'), (7, 'All 10 zł'), (8, 'All 15 zł'), (9, 'All 20 zł')], default=0, verbose_name='Wyprzedaż')),
                ('is_sale', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Nazwa slug')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Categorys')),
                ('factory_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Factory')),
                ('mark_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('material_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Material')),
                ('shop_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Produkty w sklepie',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aparat_a', models.CharField(max_length=32)),
                ('aparat_b', models.CharField(max_length=32)),
                ('battery', models.CharField(max_length=32)),
                ('system', models.CharField(max_length=32)),
                ('info', models.CharField(max_length=64)),
                ('item_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Czesc')),
                ('phone_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Telefon')),
                ('product_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Products')),
            ],
            options={
                'verbose_name_plural': 'Szczegóły produktu',
                'ordering': ('phone_id',),
            },
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
            options={
                'verbose_name_plural': 'Premie pracowników',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('hours_count', models.IntegerField(blank=True, null=True)),
                ('payment', models.IntegerField()),
                ('is_payment', models.BooleanField(default=False)),
                ('is_adv_payment', models.BooleanField(default=False)),
                ('is_bonus', models.BooleanField(default=False)),
                ('info', models.CharField(blank=True, max_length=64, null=True, verbose_name='Info')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wypłaty i inne',
                'ordering': ('date',),
            },
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
            options={
                'verbose_name_plural': 'Inne prace',
                'ordering': ('nazwa', 'pracownik'),
            },
        ),
        migrations.CreateModel(
            name='FotoProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('alt', models.CharField(blank=True, max_length=64, null=True)),
                ('used', models.BooleanField(default=False)),
                ('mini', models.BooleanField(default=False)),
                ('main', models.BooleanField(default=False)),
                ('another', models.BooleanField(default=False)),
                ('another_min', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
                ('nofoto', models.BooleanField(default=False)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Categorys')),
                ('factory_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Factory')),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Czesc')),
                ('mark_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('phone_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Telefon')),
                ('product_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.ProductDetails')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Products')),
            ],
            options={
                'verbose_name_plural': 'Zdjęcia produktów',
                'ordering': ('-id',),
            },
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
            options={
                'verbose_name_plural': 'Faktury',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='DodajSerwis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('imei', models.CharField(blank=True, max_length=15, null=True)),
                ('cena_zgoda', models.IntegerField(blank=True, default=0, null=True, verbose_name='Cena naprawy')),
                ('koszt', models.IntegerField(blank=True, default=0, null=True, verbose_name='Koszty')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('data_wydania', models.DateTimeField(blank=True, null=True)),
                ('numer_telefonu', models.CharField(blank=True, max_length=9, null=True)),
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
            options={
                'verbose_name_plural': 'Serwisy gsm',
                'ordering': ('data', 'marka', 'model'),
            },
        ),
        migrations.AddField(
            model_name='czesc',
            name='foto',
            field=models.ManyToManyField(blank=True, to='miktel.Foto', verbose_name='Foto_produktu'),
        ),
        migrations.AddField(
            model_name='czesc',
            name='marka',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka'),
        ),
        migrations.AddField(
            model_name='czesc',
            name='pracownik',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Wprowadził'),
        ),
        migrations.AddField(
            model_name='czesc',
            name='sklep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Sklep', verbose_name='Magazyn'),
        ),
        migrations.AddField(
            model_name='czesc',
            name='typ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miktel.Typ'),
        ),
        migrations.AddField(
            model_name='categorys',
            name='profile_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Profile'),
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('site_id', models.IntegerField(blank=True, choices=[(4, 'Pieczątki'), (2, 'GSM'), (5, 'Klucze'), (1, 'Home'), (3, 'Grawerowanie')], null=True, verbose_name='Strona')),
                ('title', models.CharField(max_length=128)),
                ('text', tinymce.models.HTMLField()),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Categorys')),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Czesc')),
                ('mark_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Marka')),
                ('phone_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Telefon')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Products')),
                ('profile_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miktel.Profile')),
            ],
            options={
                'verbose_name': 'Artykuły',
                'verbose_name_plural': 'Artykuły',
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
        migrations.AddIndex(
            model_name='umowakomisowanew',
            index=models.Index(fields=['phones', 'sprzedana'], name='miktel_umow_phones__c1273b_idx'),
        ),
        migrations.AddIndex(
            model_name='telefon',
            index=models.Index(fields=['sklep', 'dostepny', 'marka', 'nazwa'], name='miktel_tele_sklep_i_c42e46_idx'),
        ),
        migrations.AddIndex(
            model_name='sklep',
            index=models.Index(fields=['adres'], name='miktel_skle_adres_i_e8b51c_idx'),
        ),
        migrations.AddIndex(
            model_name='products',
            index=models.Index(fields=['category_id', 'name', 'shop_id'], name='miktel_prod_categor_a7298d_idx'),
        ),
        migrations.AddIndex(
            model_name='premiajob',
            index=models.Index(fields=['pracownik', 'sklep'], name='miktel_prem_pracown_70e8d3_idx'),
        ),
        migrations.AddIndex(
            model_name='dodajserwis',
            index=models.Index(fields=['sklep', 'status'], name='miktel_doda_sklep_i_f1ae90_idx'),
        ),
        migrations.AddIndex(
            model_name='czesc',
            index=models.Index(fields=['marka', 'typ', 'nazwa', 'sklep'], name='miktel_czes_marka_i_1994d0_idx'),
        ),
        migrations.AddIndex(
            model_name='myuser',
            index=models.Index(fields=['sklep_dzisiaj'], name='miktel_myus_sklep_d_0ba62e_idx'),
        ),
    ]
