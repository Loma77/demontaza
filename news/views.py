from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
from django.contrib.auth import logout

from account.models import Profile
from bands.models import Band


@login_required(login_url='/account/login/')
def user_create_news(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # Collecting all user pages
    user_pages = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)

    # Checking logout form
    if 'logout' in request.POST:
        logout(request)
        return redirect("/")

    # Checking search field form in navbar
    if 'site_search' in request.POST:
        name = request.POST['site_search']
        if name == '':
            name = 'all'
        return redirect("/account/search/" + str(name), name)

    content = {
        "account": "account",
        "user_create_news": "user_create_news",
        "title": 'Nova vest',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
    }
    return render(request, "news/create_news.html", content)
