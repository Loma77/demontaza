from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from random import choice

from bands.models import Band


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def home_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    bands = Band.objects.all()
    bands_list = []

    while len(bands_list) < 5:
        band = choice(bands)
        if band in bands_list:
            pass
        else:
            if band.band_picture:
                bands_list.append(band)
            else:
                pass

    content = {
        "home": "home",
        "title": "Demontaža",
        "bands_list": bands_list,
    }
    return render(request, "home/home_page.html", content)


def help_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    content = {
        "help_page": "help_page",
        "title": "Pomoć"
    }
    return render(request, "home/help_page.html", content)
