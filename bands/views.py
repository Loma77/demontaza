import os
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import login_required
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.http import JsonResponse
import requests

from .models import Genre, Band
from account.models import Profile, Location

from .forms import EditBand, BandLogoForm, BandPictureForm, CreateBand


def band_search_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    # Collecting all bands from database
    bends = Band.objects.all()

    # Collecting all active locations
    mesto = []
    for b in bends:
        if b.city_or_town not in mesto:
            mesto.append(b.city_or_town)
        else:
            pass

    # Collecting all active genres
    zanr = []
    for b in bends:
        if b.genre not in zanr:
            zanr.append(b.genre)
        else:
            pass

    # Sorting all collected locations and genres
    mesto.sort(key=lambda x: x.place)
    zanr.sort(key=lambda x: x.genre)

    # AJAX form
    if request.is_ajax():
        band_genre = request.POST['genre']
        band_location = request.POST['location']
        if band_genre != '--' and band_location != '--':
            search = Band.objects.filter(genre=band_genre, city_or_town=band_location)
        elif band_genre != '--' and band_location == '--':
            search = Band.objects.filter(genre=band_genre)
        elif band_genre == '--' and band_location != '--':
            search = Band.objects.filter(city_or_town=band_location)
        else:
            search = bends

        if band_genre != '--':
            genre = Genre.objects.get(id=band_genre)
        else:
            genre = '--'
        if band_location != '--':
            location = Location.objects.get(id=band_location)
        else:
            location = '--'

        content_search = {
            "search": search,
            "mesto": mesto,
            "zanr": zanr,
            "band_genre": genre,
            "band_location": location,
        }
        html = render_to_string("bands/band_search_ajax.html", content_search, request=request)
        return JsonResponse({'form': html})

    content = {
        "title": "Pretraga",
        "band_search": "band_search",
        "bends": len(bends),
        "mesto": mesto,
        "zanr": zanr,
        "ime": "all",
        "search": bends,
    }
    return render(request, "bands/band_search_page.html", content)


def band_page(request, band_id):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    band_profile = None
    name = "Bend ne postoji"

    try:
        band_profile = Band.objects.get(id=band_id)
    except Band.DoesNotExist:
        pass

    if band_profile:
        name = band_profile.name

    content = {
        "title": name + " | Demontaža",
        "band_profile": band_profile,
    }
    return render(request, "bands/band_page.html", content)


@login_required(login_url='/account/login/')
def account_band_search_page(request):
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

    # Collecting all bands from database
    bends = Band.objects.all()

    # Collecting all active locations
    mesto = []
    for b in bends:
        if b.city_or_town not in mesto:
            mesto.append(b.city_or_town)
        else:
            pass

    # Collecting all active genres
    zanr = []
    for b in bends:
        if b.genre not in zanr:
            zanr.append(b.genre)
        else:
            pass

    # Sorting all collected locations and genres
    mesto.sort(key=lambda x: x.place)
    zanr.sort(key=lambda x: x.genre)

    # AJAX form
    if request.is_ajax():
        band_genre = request.POST['genre']
        band_location = request.POST['location']
        if band_genre != '--' and band_location != '--':
            search = Band.objects.filter(genre=band_genre, city_or_town=band_location)
        elif band_genre != '--' and band_location == '--':
            search = Band.objects.filter(genre=band_genre)
        elif band_genre == '--' and band_location != '--':
            search = Band.objects.filter(city_or_town=band_location)
        else:
            search = bends

        if band_genre != '--':
            genre = Genre.objects.get(id=band_genre)
        else:
            genre = '--'
        if band_location != '--':
            location = Location.objects.get(id=band_location)
        else:
            location = '--'

        content_search = {
            "account": "account",
            "search": search,
            "mesto": mesto,
            "zanr": zanr,
            "band_genre": genre,
            "band_location": location,
        }
        html = render_to_string("bands/band_search_ajax.html", content_search, request=request)
        return JsonResponse({'form': html})

    content = {
        "account": "account",
        "title": "Pretraga",
        "band_search": "band_search",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "bends": len(bends),
        "search": bends,
        "ime": "all",
        "mesto": mesto,
        "zanr": zanr,
    }
    return render(request, "bands/band_search_page.html", content)


@login_required(login_url='/account/login/')
def account_create_band_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = CreateBand(request.POST or None)

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

    genre = Genre.objects.all()
    location = Location.objects.all()

    if request.method == 'POST' or None:
        form = CreateBand(request.POST, request.FILES)
        if form.is_valid():
            band_name = form.cleaned_data['name']
            logo = form.cleaned_data['logo']
            band_picture = form.cleaned_data['band_picture']
            genre = form.cleaned_data['genre']
            city_or_town = form.cleaned_data['city_or_town']
            year_of_creation = form.cleaned_data['year_of_creation']
            members = form.cleaned_data['members']
            bio = form.cleaned_data['bio']
            activity = form.cleaned_data['activity']
            yt_video1 = form.cleaned_data['yt_video1']
            yt_video2 = form.cleaned_data['yt_video2']
            yt_video3 = form.cleaned_data['yt_video3']
            youtube = form.cleaned_data['youtube']
            facebook = form.cleaned_data['facebook']
            soundcloud = form.cleaned_data['soundcloud']
            instagram = form.cleaned_data['instagram']
            bandcamp = form.cleaned_data['band_camp']

            b = Band(creator=user, name=band_name, genre=genre, logo=logo, band_picture=band_picture,
                     city_or_town=city_or_town, year_of_creation=year_of_creation, members=members, bio=bio,
                     activity=activity, yt_video1=yt_video1, yt_video2=yt_video2, yt_video3=yt_video3, youtube=youtube,
                     facebook=facebook, soundcloud=soundcloud, instagram=instagram, band_camp=bandcamp)

            os.listdir()

            if b.logo:
                b.create_logo()
            if b.band_picture:
                b.create_picture()
            b.save()

            # RENAMING AND UPDATING PATH FOR LOGO AND BAND PICTURE
            if logo:
                os.rename('media/logo/' + str(b.creator.id) +
                          '/None/', 'media/logo/' + str(b.creator.id) + '/' + str(b.id) + '/')

                Band.objects.filter(name=band_name,
                                    city_or_town=city_or_town).update(logo='logo/'+str(b.creator.id) + '/'+str(b.id)+'/'+str(logo))

            if band_picture:
                os.rename('media/band_picture/' + str(b.creator.id) +
                          '/None/', 'media/band_picture/' + str(b.creator.id) + '/' + str(b.id) + '/')

                Band.objects.filter(name=band_name,
                                    city_or_town=city_or_town).update(band_picture='band_picture/'+str(b.creator.id)+'/'+str(b.id)+'/'+str(band_picture))

            return redirect("/band/account/page/" + str(b.id), b.id)

    content = {
        "account": "account",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "genre": genre,
        "location": location,
        "form": form,
        "title": "Create Band | Demontaža",
    }
    return render(request, "bands/band_create_page.html", content)


@login_required(login_url='/account/login/')
def account_band_page(request, band_id):
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

    try:
        band_profile = Band.objects.get(id=band_id)
    except Band.DoesNotExist:
        return redirect('/account/home/')

    followers = band_profile.users_follow.all()
    band_followers = []
    for follower in followers:
        band_followers.append(Profile.objects.get(user=follower))

    # Deleting band page
    if 'delete' in request.POST:
        instance = Band.objects.get(id=band_id)
        instance.delete_logo()
        instance.delete_picture()

        instance.delete()
        return redirect("/account/home/")

    # AJAX form
    if request.is_ajax():
        yes_or_no = request.POST['id']
        if yes_or_no == "yes":
            band_profile.users_follow.add(request.user)
            followers = band_profile.users_follow.all()
            band_followers = []
            for follower in followers:
                band_followers.append(Profile.objects.get(user=follower))

            content = {
                "account": "account",
                "band_profile": band_profile,
                "band_followers": band_followers,
            }
            html = render_to_string("bands/band_check_follow.html", content, request=request)
            return JsonResponse({'form': html})
        elif yes_or_no == "no":
            band_profile.users_follow.remove(request.user)
            followers = band_profile.users_follow.all()
            band_followers = []
            for follower in followers:
                band_followers.append(Profile.objects.get(user=follower))

            content = {
                "account": "account",
                "band_profile": band_profile,
                "band_followers": band_followers,
            }
            html = render_to_string("bands/band_check_follow.html", content, request=request)
            return JsonResponse({'form': html})

    content = {
        "account": "account",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "title": band_profile.name + " | Demontaža",
        "band_profile": band_profile,
        "band_followers": band_followers,
    }
    return render(request, "bands/band_page.html", content)


@login_required(login_url='/account/login/')
def account_band_edit_page(request, band_id):
    user = request.user
    profile = Profile.objects.get(user=user)

    # Checking administration permission for editing a band data
    try:
        band_profile = Band.objects.get(id=band_id)
        band_admins = band_profile.admins.all()
        if user != band_profile.creator and user not in band_admins:
            return redirect('/band/account/page/' + str(band_id), band_id)
    except:
        return redirect('/band/account/page/' + str(band_id), band_id)

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

    genre = Genre.objects.all()
    location = Location.objects.all()
    # Forms for editing the band
    form = EditBand(request.POST or None, instance=band_profile)
    form_logo = BandLogoForm(request.POST or None, instance=band_profile)
    form_picture = BandPictureForm(request.POST or None, instance=band_profile)

    if 'profil' in request.POST:
        form = EditBand(request.POST, instance=band_profile)
        form_logo = BandLogoForm(request.POST, request.FILES, instance=band_profile)
        form_picture = BandPictureForm(request.POST, request.FILES, instance=band_profile)
        if 'logo' in request.FILES:
            band_profile.delete_logo()
        if 'band_picture' in request.FILES:
            band_profile.delete_picture()
        if form_logo.is_valid():
            form_logo.save()
        if form_picture.is_valid():
            form_picture.save()
        if form.is_valid():
            name = form.cleaned_data['name']
            genre = form.cleaned_data['genre']
            city_or_town = form.cleaned_data['city_or_town']
            year_of_creation = form.cleaned_data['year_of_creation']
            members = form.cleaned_data['members']
            bio = form.cleaned_data['bio']
            activity = form.cleaned_data['activity']
            yt_video1 = form.cleaned_data['yt_video1']
            yt_video2 = form.cleaned_data['yt_video2']
            yt_video3 = form.cleaned_data['yt_video3']
            youtube = form.cleaned_data['youtube']
            facebook = form.cleaned_data['facebook']
            soundcloud = form.cleaned_data['soundcloud']
            instagram = form.cleaned_data['instagram']
            bandcamp = form.cleaned_data['band_camp']

            Band.objects.filter(id=band_id).update(name=name, genre=genre, city_or_town=city_or_town,
                                                   year_of_creation=year_of_creation, members=members, bio=bio,
                                                   activity=activity, youtube=youtube, yt_video1=yt_video1,
                                                   yt_video2=yt_video2, yt_video3=yt_video3, facebook=facebook,
                                                   soundcloud=soundcloud, instagram=instagram, band_camp=bandcamp)
            return redirect("/band/account/page/" + str(band_id), band_id)

    content = {
        "account": "account",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "band_profile": band_profile,
        "genre": genre,
        "location": location,
        "title": "Edit Band | Demontaža",
        "form": form,
        "form_logo": form_logo,
        "form_picture": form_picture,
    }
    return render(request, "bands/band_edit_page.html", content)


@login_required(login_url='/account/login/')
def account_band_admins_page(request, band_id):
    user = request.user
    profile = Profile.objects.get(user=user)

    # Checking administration permission for editing a band data
    try:
        band_profile = Band.objects.get(id=band_id)
        band_admins = band_profile.admins.all()
        if user != band_profile.creator and user not in band_admins:
            return redirect('/band/account/page/' + str(band_id), band_id)
    except:
        return redirect('/band/account/page/' + str(band_id), band_id)

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

    # AJAX form
    if request.is_ajax():
        remove_or_add = request.POST['name']
        if remove_or_add == "remove_admin":
            admin = request.POST['id']
            band_profile.admins.remove(admin)

        elif remove_or_add == "add_admin":
            admin = request.POST['id']
            if admin in band_admins:
                pass
            else:
                band_profile.admins.add(admin)

        content = {
            "account": "account",
            "user": user,
            "profile": profile,
            "band_profile": band_profile,
        }
        html = render_to_string("bands/band_admins_ajax.html", content, request=request)
        return JsonResponse({'form': html})

    content = {
        "account": "account",
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "band_profile": band_profile,
        "title": "Band Admins | Demontaža",
    }
    return render(request, "bands/band_admins_page.html", content)
