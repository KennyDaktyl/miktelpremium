Status_User = (
    (0, "Właścicel"),
    (1, "Pracownik"),
    (2, "Osoba zewnętrzna"),
)
STRONY = {
    (1, "Home"),
    (2, "GSM"),
    (3, "Grawerowanie"),
    (4, "Pieczątki"),
    (5, "Klucze"),
}
Rodzaj_Umowy = (
    (0, "Umowa o prace"),
    (1, "Umowa zlecenie"),
    (2, "Brak danych"),
)
STATUS_NAPRAWY = (
    (1, "Przyjęty na seriws"),
    (2, "W naprawie"),
    (3, "Oczekuje na decyzję klienta"),
    (4, "Gotowy do odbioru"),
    (5, "Wydany"),
    (6, "Poprawka"),
    (7, "Reklamacja"),
)

StanTelefonu = ((0, "Nowy"), (1, "Używany"), (2, "Bez pudełka"))

StanCzesci = ((0, "Nowy"), (1, "Używany"), (2, "Zamiennik"), (3,
                                                              "Z demontażu"))
Kolor = ((0, "Czarny"), (1, "Biały"), (2, "Złoty"), (3, "Niebieski"), (4,
                                                                       "Inny"))

RODZAJ_PROWIZJI = (
    (0, "Procent"),
    (1, "cena/szt"),
)

MIESIACE = (
    (1, "Styczen"),
    (2, "Luty"),
    (3, "Marzec"),
    (4, "Kwiecień"),
    (5, "Maj"),
    (6, "Czerwiec"),
    (7, "Lipiec"),
    (8, "Sierpień"),
    (9, "Wrzesień"),
    (10, "Poździernik"),
    (11, "Listopad"),
    (12, "Grudzień"),
)

ROK = (
    (1, "2019"),
    (2, "2020"),
    (3, "2021"),
    (4, "2022"),
    (5, "2023"),
    (5, "2024"),
)

OD_KOGO = ((0, "Z hurtownii"), (1, "Od klienta"))

STAN = ((0, "Nowy"), (1, "Używany"), (2, "Refurb"), (3, "Bez pudełka"))

IloscRekordow = ((2, 2), (10, 10), (50, 50), (100, 100), (200, 200), (500,
                                                                      500))

SALE = ((0, "Nie"), (1, "Sale -10%"), (2, "Sale -20%"), (3, "Sale -30%"),
        (4, "Sale -40%"), (5, "Sale -50%"), (6, "All 5 zł"), (7, "All 10 zł"),
        (8, "All 15 zł"), (9, "All 20 zł"))
SALE_SORTED = sorted(SALE)
