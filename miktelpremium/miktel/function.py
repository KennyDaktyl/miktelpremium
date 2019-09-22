import os
import smtplib
from googlevoice.util import input
from googlevoice import Voice
from smsapi.client import SmsApiPlClient
from miktel.models import UmowaKomisowaNew

from datetime import datetime

rok = datetime.now().year
miesiac = datetime.now().month

ACCESS_TOKEN_SMS = os.environ.get('ACCESS_TOKEN_SMS')
gmail_user = os.environ.get('GMAIL_USER')
gmail_password = os.environ.get('GMAIL_PASSWORD')


def numer_umowy():
    # number = ""
    today_month = datetime.now().month

    # last_number = UmowaKomisu.objects.get(number="020/09/2019")
    last_number = UmowaKomisowaNew.objects.last()
    print(last_number)
    # today_month = 1
    if not last_number:
        number_set = "001"
        number_indx = int(number_set)
        print("jestem w not")
    else:
        number_indx = int(last_number.number[:3]) + int(1)
        print(int(last_number.number[:3]) + int(1))
        data = last_number.data_zak.month
        print(data)
        print("Jestem w else")
        if today_month != data:
            number_indx = 1
            print("jestem w else if")
    number = (str(number_indx), "/", str(miesiac), "/", str(rok))
    if number_indx < 10:
        number_format = f"00{number_indx} / {miesiac} / {rok}"
    if 100 > number_indx > 9:
        number_format = f"0{number_indx} / {miesiac} / {rok}"
    if number_indx > 99:
        number_format = f"{number_indx} / {miesiac} / {rok}"
    print(number_format)
    return number_format


client = SmsApiPlClient(access_token=ACCESS_TOKEN_SMS)


def send(to, message):

    send_results = client.sms.send(to=to, message=message)

    for result in send_results:
        print(result.id, result.status, result.points, result.error)
    return send_results


def saldo_sms():
    r = client.account.balance()

    return r.points


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def send_email(subject, text):
    user = gmail_user
    password = gmail_password
    FROM = 'miktelgsm@miktelgsm.pl'
    TO = ['kennydak@interia.pl']
    SUBJECT = strip_non_ascii(subject)
    TEXT = strip_non_ascii(text)

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.miktelgsm.nazwa.pl", 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail(FROM, TO, message)
    server.close()
