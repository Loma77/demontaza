import os
from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
from django.contrib.auth import logout

from .models import News
from account.models import Profile
from bands.models import Band

from .forms import CreateNews, NewsPictureForm


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

    # Checking friend requests
    friend_requests = []
    all_users = Profile.objects.all()
    for u in all_users:
        if user in u.friends.all():
            if u.user in profile.friends.all():
                pass
            else:
                friend_requests.append(u.user)
        else:
            pass

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
        "friend_requests": friend_requests,
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

    # Checking friend requests
    friend_requests = []
    all_users = Profile.objects.all()
    for u in all_users:
        if user in u.friends.all():
            if u.user in profile.friends.all():
                pass
            else:
                friend_requests.append(u.user)
        else:
            pass

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
        "friend_requests": friend_requests,
    }
    return render(request, "news/create_news.html", content)


@login_required(login_url='/account/login/')
def news_display_page(request, news_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    news = News.objects.get(id=news_id)

    # Collecting all user pages
    user_pages = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)

    # Checking friend requests
    friend_requests = []
    all_users = Profile.objects.all()
    for u in all_users:
        if user in u.friends.all():
            if u.user in profile.friends.all():
                pass
            else:
                friend_requests.append(u.user)
        else:
            pass

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

    # Deleting news
    if 'delete' in request.POST:
        instance = News.objects.get(id=news_id)
        instance.delete_picture()
        instance.delete()
        return redirect("/account/home/")

    content = {
        "account": "account",
        "news_display": "news_display",
        "title": "Prikaz vesti",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "news_data": news,
        "friend_requests": friend_requests,
    }
    return render(request, "news/news_page.html", content)


@login_required(login_url='/account/login/')
def user_edit_news(request, news_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    news = News.objects.get(id=news_id)

    form = CreateNews(request.POST or None, instance=news)
    form_picture = NewsPictureForm(request.POST or None, instance=news)

    # Collecting all user pages
    user_pages = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)

    # Checking friend requests
    friend_requests = []
    all_users = Profile.objects.all()
    for u in all_users:
        if user in u.friends.all():
            if u.user in profile.friends.all():
                pass
            else:
                friend_requests.append(u.user)
        else:
            pass

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

    if 'brisi_sliku' in request.POST:
        form_picture = NewsPictureForm(request.POST, request.FILES, instance=news)
        news.delete_picture()

    if 'news_create' in request.POST:
        form = CreateNews(request.POST, instance=news)
        form_picture = NewsPictureForm(request.POST, request.FILES, instance=news)
        if 'news_picture' in request.FILES:
            news.delete_picture()
        if form_picture.is_valid():
            form_picture.save()
        if form.is_valid():
            title = form.cleaned_data['title']
            news = form.cleaned_data['news']
            yt_video = form.cleaned_data['yt_video']
            fb_event = form.cleaned_data['fb_event']

            News.objects.filter(id=news_id).update(title=title, news=news, yt_video=yt_video, fb_event=fb_event)

            return redirect("/news/display/" + str(news_id), news_id)

    content = {
        "account": "account",
        "user_edit_news": "user_edit_news",
        "title": 'Uredi objavu',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "form": form,
        "form_picture": form_picture,
        "news_data": news,
        "friend_requests": friend_requests,
    }
    return render(request, "news/create_news.html", content)


@login_required(login_url='/account/login/')
def band_edit_news(request, band_id, news_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    band = Band.objects.get(id=band_id)
    news = News.objects.get(id=news_id)

    form = CreateNews(request.POST or None, instance=news)
    form_picture = NewsPictureForm(request.POST or None, instance=news)

    # Collecting all user pages
    user_pages = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)

    # Checking friend requests
    friend_requests = []
    all_users = Profile.objects.all()
    for u in all_users:
        if user in u.friends.all():
            if u.user in profile.friends.all():
                pass
            else:
                friend_requests.append(u.user)
        else:
            pass

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

    if 'brisi_sliku' in request.POST:
        form_picture = NewsPictureForm(request.POST, request.FILES, instance=news)
        news.delete_picture()

    if 'news_create' in request.POST:
        form = CreateNews(request.POST, instance=news)
        form_picture = NewsPictureForm(request.POST, request.FILES, instance=news)
        if 'news_picture' in request.FILES:
            news.delete_picture()
        if form_picture.is_valid():
            form_picture.save()
        if form.is_valid():
            title = form.cleaned_data['title']
            news = form.cleaned_data['news']
            yt_video = form.cleaned_data['yt_video']
            fb_event = form.cleaned_data['fb_event']

            News.objects.filter(id=news_id).update(title=title, news=news, yt_video=yt_video, fb_event=fb_event)

            return redirect("/news/display/" + str(news_id), news_id)

    content = {
        "account": "account",
        "band_edit_news": "band_edit_news",
        "band": band,
        "title": 'Uređivanje vesti | bend',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "form": form,
        "form_picture": form_picture,
        "news_data": news,
        "friend_requests": friend_requests,
    }
    return render(request, "news/create_news.html", content)
