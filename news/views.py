import os
from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
from django.contrib.auth import logout

from .models import News
from account.models import Profile
from bands.models import Band

from .forms import CreateNews


@login_required(login_url='/account/login/')
def user_create_news(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    form = CreateNews(request.POST or None)

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

    if request.method == 'POST' or None:
        form = CreateNews(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            news = form.cleaned_data['news']
            news_picture = form.cleaned_data['news_picture']
            yt_video = form.cleaned_data['yt_video']
            fb_event = form.cleaned_data['fb_event']

            n = News(creator=user, title=title, news=news, news_picture=news_picture,
                     yt_video=yt_video, fb_event=fb_event)

            os.listdir()

            if n.news_picture:
                n.create_news_picture()
            n.save()

            # RENAMING AND UPDATING PATH FOR NEWS PICTURE
            if news_picture:
                os.rename('media/news_picture/' + str(n.creator.id) +
                          '/None/', 'media/news_picture/' + str(n.creator.id) + '/' + str(n.id) + '/')

                News.objects.filter(id=n.id).update(news_picture='news_picture/' + str(n.creator.id) + '/' + str(n.id) + '/' + str(news_picture))

            return redirect("/account/home/")

    content = {
        "account": "account",
        "user_create_news": "user_create_news",
        "title": 'Nova objava',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "form": form,
    }
    return render(request, "news/create_news.html", content)


@login_required(login_url='/account/login/')
def band_create_news(request, band_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    band = Band.objects.get(id=band_id)

    form = CreateNews()

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

    if request.method == 'POST' or None:
        form = CreateNews(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            news = form.cleaned_data['news']
            news_picture = form.cleaned_data['news_picture']
            yt_video = form.cleaned_data['yt_video']
            fb_event = form.cleaned_data['fb_event']

            n = News(creator=user, band=band, title=title, news=news, news_picture=news_picture,
                     yt_video=yt_video, fb_event=fb_event)

            os.listdir()

            if n.news_picture:
                n.create_news_picture()
            n.save()

            # RENAMING AND UPDATING PATH FOR NEWS PICTURE
            if news_picture:
                os.rename('media/news_picture/' + str(n.creator.id) +
                          '/None/', 'media/news_picture/' + str(n.creator.id) + '/' + str(n.id) + '/')

                News.objects.filter(id=n.id).update(news_picture='news_picture/' + str(n.creator.id) + '/' + str(n.id) + '/' + str(news_picture))

            return redirect("/account/home/")

    content = {
        "account": "account",
        "band_create_news": "band_create_news",
        "band": band,
        "title": 'Nova vest | bend',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "form": form,
    }
    return render(request, "news/create_news.html", content)
