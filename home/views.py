from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


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

    content = {
        "home": "home",
        "title": "Demontaža",
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
