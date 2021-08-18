from django.conf import settings
from django.core.mail import send_mail
import os
import smtplib
from googlevoice import *
from googlevoice import Voice
from smsapi.client import SmsApiPlClient
from smsapi.exception import SmsApiException
from miktel.models import UmowaKomisowaNew, WorkSchedule

from datetime import datetime


ACCESS_TOKEN_SMS = os.environ.get('TOKEN_SMS')
gmail_user = os.environ.get('GMAIL_USER')
gmail_password = os.environ.get('GMAIL_PASSWORD')


def numer_umowy():
    # number = ""
    today_month = datetime.now().month
    rok = datetime.now().year
    miesiac = datetime.now().month
    # last_number = UmowaKomisu.objects.get(number="020/09/2019")
    last_number = UmowaKomisowaNew.objects.first()
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
        number_format = f"00{number_indx}/{miesiac}/{rok}"
    if 100 > number_indx > 9:
        number_format = f"0{number_indx}/{miesiac}/{rok}"
    if number_indx > 99:
        number_format = f"{number_indx}/{miesiac}/{rok}"
    print(number_format)
    return number_format


client = SmsApiPlClient(access_token=ACCESS_TOKEN_SMS)


def send(to, message):

    try:
        send_results = client.sms.send(to=to, message=message)

        for result in send_results:
            print(result.id, result.points, result.error)
    except:
        pass
    # try:
    #     contact = client.sms.send(to=to)
    # except SmsApiException as e:
    #     print(e.message, e.code)

    # return send_results


def saldo_sms():
    r = client.account.balance()

    return r.points


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'raihncse@gmail.com'
# DEFAULT_FROM_EMAIL = 'raihncse@gmail.com'
# SERVER_EMAIL = 'raihncse@gmail.com'
# EMAIL_HOST_PASSWORD = '**************'
def send_email(subject, text):
    user = gmail_user
    password = gmail_password
    FROM = user
    TO = ['miktelgsm@miktelgsm.pl']
    SUBJECT = strip_non_ascii(subject)
    TEXT = strip_non_ascii(text)

    # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #         """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    send_mail(subject, text, settings.EMAIL_HOST_USER,
              [settings.EMAIL_HOST_USER])

    # server = smtplib.SMTP("smtp.miktelgsm.nazwa.pl", 587)
    # server.ehlo()
    # server.starttls()
    # server.login(user, password)
    # server.sendmail(FROM, TO, message)
    # server.close()


def hours_count():
    from datetime import datetime, timedelta
    schedule = WorkSchedule.objects.all()
    for el in schedule:
        if el.time_start and el.time_end != None:
            time_start_h = str(el.time_start)[0:2]
            time_start_m = str(el.time_start)[3:5]
            time_end_h = str(el.time_end)[0:2]
            time_end_m = str(el.time_end)[3:5]
            el.time_duration = str(
                timedelta(hours=int(time_end_h), minutes=int(time_end_m)) -
                timedelta(hours=int(time_start_h), minutes=int(time_start_m)))
            print(el)
            el.save()


def hours_in_mount(user, schedule):
    hours = 0
    for sch in schedule:
        if sch.time_duration != None:
            hours += int(sch.time_duration.hour) + int(
                sch.time_duration.minute)
            # print(int(sch.time_duration.hour))
            # print(int(sch.time_duration.minute))
    return hours
