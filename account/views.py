from random import choice
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.contrib.auth.views import login_required
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.http import JsonResponse
import difflib
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse

from .forms import LoginForm, UserRegistrationForm, ForgotPasswordForm, ChangePassword, UserEditForm, ProfileEditForm
from .models import Profile

from bands.models import Band, Genre
from news.models import News


def get_user(email):
    try:
        user = User.objects.get(email=email.lower())
        return user.username
    except User.DoesNotExist:
        return None


def login_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    form_login = LoginForm(request.POST or None)

    if form_login.is_valid():
        # login user
        cd = form_login.cleaned_data
        email = cd['email']
        password = cd['password']
        username = get_user(email)
        user = authenticate(username=username, password=password)

        last = user.last_login
        login(request, user)

        try:
            Profile.objects.filter(user=user).update(last_time_login=last)
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, last_time_login=last)

        return redirect("/account/home/")

    content = {
        "login_page": "login_page",
        "title": "Login",
        "login_form": form_login,
    }
    return render(request, "account/login_page.html", content)


def forgot_password_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    form = ForgotPasswordForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data
        password = ''
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while len(password) < 8:
            char = choice(alphabet)
            password += char
        u = User.objects.get(email=email)
        u.set_password(password)
        u.save()
        subject = f"Nova lozinka"
        message = ''

        html_content = f"<a href='#' style='text-decoration: none;'><h2 " \
                       f"style='background-image: linear-gradient(to right, #007BFF,grey,black,grey,#007BFF); " \
                       f"color:white; text-align:center; padding:5px;'>DEMONTAŽA</h2></a><hr>" \
                       f"<p>Poštovani korisniče <b>{u.first_name} {u.last_name}</b>,</p>" \
                       f"<p>upravo ste promenili svoju lozinku.</p>" \
                       f"<p>Vaša nova lozinka je: <strong>{password}</strong></p>" \
                       f"<p>Molimo vas da sačuvate ovu lozinku dok se ne prijavite sledeći put.</p>" \
                       f'<p>Možete je promeniti u "Podešavanje Naloga", pod-meni "Promeni Lozinku" kada se prijavite' \
                       f' na vaš nalog.</p><br>' \
                       f'<p><em>Ukoliko niste vi tražili promenu vaše lozinke, molimo vas da nas kontaktirate da bi ' \
                       f'rešili ovu nastalu situaciju.<em></p>' \
                       f"<hr><a href='#' style='text-decoration: none;'>" \
                       f"<p style='text-align:center; color:grey;'><small>&copy; Demontaža 2021" \
                       f"</small></p></a>"

        from_email = 'support@demontaza.rs'
        try:
            msg = EmailMultiAlternatives(subject, message, from_email, [u.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except BadHeaderError:
            return HttpResponse("Email nije poslat. Pokušajte ponovo ili nas kontaktirajte.")
        return redirect("/account/login")

    content = {
        "title": "Zaboravio sam lozinku",
        "form": form,
    }
    return render(request, 'account/forgot_password_page.html', content)


def create_account_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    user_form = UserRegistrationForm(request.POST or None)

    if user_form.is_valid():
        # Create a new user object but avoid saving it yet
        new_user = user_form.save(commit=False)
        # Set the chosen password
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.username = user_form.cleaned_data['email']
        # Save the User object
        new_user.save()
        # Add user to group
        my_group = Group.objects.get(name='Korisnik')
        my_group.user_set.add(new_user)
        # Create the user profile
        Profile.objects.create(user=new_user)

        # LOGIN AFTER CREATION
        user = authenticate(username=user_form.cleaned_data['email'],
                            password=user_form.cleaned_data['password'])
        login(request, user)

        return redirect("/account/home/")

    content = {
        "account_page": "account_page",
        "title": "Kreiranje naloga",
        "user_form": user_form
    }

    return render(request, "account/create_account_page.html", content)


@login_required(login_url='/account/login/')
def account_home_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)

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

    # Collecting all news
    guest_news = []
    news = News.objects.all().order_by('-updated')

    for n in news:
        news_user_profile = Profile.objects.get(user=n.creator)
        if user in news_user_profile.friends.all() and n.creator in profile.friends.all() or user == n.creator:
            guest_news.append(n)

    content = {
        "account": "account",
        "account_home": "account_home",
        "title": 'Demontaža',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "guest_news": guest_news,
        "guest_user": user,
        "friend_requests": friend_requests,
    }
    return render(request, "account/account_home.html", content)


@login_required(login_url='/account/login/')
def account_profile_page(request, user_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    guest_user = User.objects.get(id=user_id)
    guest_profile = Profile.objects.get(user=guest_user)
    guest_news = News.objects.filter(creator=guest_user).order_by('-updated')

    # Collecting all user pages and all pages that user follows
    user_pages = []
    user_follows = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)
        for b in bands:
            if user in b.users_follow.all():
                user_follows.append(b)

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

    # Checking user search field form
    if 'site_search' in request.POST:
        name = request.POST['site_search']
        if name == '':
            name = 'all'
        return redirect("/account/search/" + str(name), name)

    # AJAX form
    if request.is_ajax():
        task = request.POST['task']
        friend_id = request.POST['id']
        friend_user = User.objects.get(id=friend_id)
        if task == "unfriend":
            profile.friends.remove(friend_user)
            guest_profile.friends.remove(user)

        elif task == "remove_request":
            profile.friends.remove(friend_user)

        elif task == 'accept_request' or task == 'send_request':
            profile.friends.add(friend_user)

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

        content = {
            "account": "account",
            "user": user,
            "profile": profile,
            "guest_user": guest_user,
            "guest_profile": guest_profile,
            "guest_news": guest_news,
            "friend_requests": friend_requests,
        }
        html = render_to_string("account/account_profile_ajax.html", content, request=request)
        html1 = render_to_string("account/account_profile_info_ajax.html", content, request=request)
        html2 = render_to_string("account/refresh_friend_request_ajax.html", content, request=request)
        html3 = render_to_string("account/refresh_friend_request_modal_ajax.html", content, request=request)
        return JsonResponse({'form': html, 'info': html1, 'new_req': html2, 'refresh_modal': html3})

    content = {
        "account": "account",
        "account_profile": "account_profile",
        "title": guest_user.first_name + ' ' + guest_user.last_name + ' | Demontaža',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "user_follows": user_follows,
        "guest_user": guest_user,
        "guest_profile": guest_profile,
        "guest_news": guest_news,
        "users": User.objects.filter(groups__name='Korisnik').exclude(id=user.id),
        "friend_requests": friend_requests,
    }
    return render(request, "account/account_profile.html", content)


@login_required(login_url='/account/login/')
def account_settings_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form_password = ChangePassword(user=user)

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

    form_user = UserEditForm(request.POST or None, instance=user)
    form_picture = ProfileEditForm(request.POST or None, instance=profile)

    # Profile Picture forms
    if 'changePicture' in request.POST:
        form_picture = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form_picture.is_valid():
            profile.delete_picture_path()
            profile.create()
            form_picture.save()
            return redirect("/account/settings/")

    # Change user data forms
    if 'changePersonal' in request.POST:
        if form_user.is_valid():
            form_user.save()
            return redirect("/account/settings/")

    # Changing password form
    if 'changePassword' in request.POST:
        form_password = ChangePassword(data=request.POST, user=user)
        if form_password.is_valid():
            form_password.save()
            update_session_auth_hash(request, form_password.user)
            return redirect("/account/settings/")
        else:
            form_user = UserEditForm(initial={'first_name': user.first_name,
                                              'last_name': user.last_name,
                                              'email': user.email})
            content_new = {
                "account": "account",
                "account_settings": "account_settings",
                "title": user.first_name + ' ' + user.last_name + ' | Demontaža',
                "user": user,
                "profile": profile,
                "user_pages": user_pages,
                "form_user": form_user,
                "form_picture": form_picture,
                "form_password": form_password,
                "password_error": "password_error",
            }
            return render(request, "account/account_settings.html", content_new)

    content = {
        "account": "account",
        "account_settings": "account_settings",
        "title": user.first_name + ' ' + user.last_name + ' | Demontaža',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "form_user": form_user,
        "form_picture": form_picture,
        "form_password": form_password,
        "friend_requests": friend_requests,
    }
    return render(request, "account/account_settings.html", content)


@login_required(login_url='/account/login/')
def account_interest(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    genre = Genre.objects.all()

    interests = []

    """
    # POPUNJAVANJE LISTE INTERESOVANJA PO LAJKOVIMA KORISNIKA
    for like in likes:
        b = Band.objects.get(band_name=like.band.band_name, city_or_town=like.band.city_or_town)
        try:
            n = BandNews.objects.filter(band=b)
            for k in n:
                if k.news:
                    interest.append(b)
        except BandNews.DoesNotExist:
            pass

    # POPUNJAVANJE LISTE INTERESOVANJA PO INTERESOVANJIMA KORISNIKA
    if personal_interest:
        for i in personal_interest:
            try:
                b = Band.objects.filter(genre=i.genre)
                for k in b:
                    try:
                        n = BandNews.objects.filter(band=k)
                        for j in n:
                            if j.news:
                                interest.append(k)
                    except BandNews.DoesNotExist:
                        pass
            except Band.DoesNotExist:
                pass

    interest = list(dict.fromkeys(interest))

    latest_news = []

    for late in interest:
        for la in BandNews.objects.raw("SELECT * "
                                       "FROM modeli_bandnews n "
                                       "LEFT JOIN modeli_band b "
                                       "ON n.band_id = b.id WHERE b.id =" + str(late.id)):
            latest_news.append(la)

    latest_news.sort(key=sorting, reverse=True)

    # popunjavanje NOVOSTI
    novosti = []
    try:
        last_login = LastLogin.objects.get(user=user)
        for novost in latest_news:
            if novost.updated_at > last_login.last_login:
                novosti.append(novost)
    except LastLogin.DoesNotExist:
        pass

    try:
        last_login = LastLogin.objects.get(user=user)
        commented_news_id = Comment.objects.filter(user=user).values_list('news_id', flat=True).distinct()

        for new_novost in commented_news_id:
            for com in Comment.objects.raw("SELECT * "
                                           "FROM modeli_comment "
                                           "WHERE NOT user_id = " + str(user.id) + " "
                                           "AND news_id = " + str(new_novost) + " "
                                           "AND created > '" + str(last_login.last_login) + "' "
                                           "ORDER BY created"):
                novosti.append(com)
    except LastLogin.DoesNotExist:
        pass

    genre = Genre.objects.raw("SELECT * "
                              "FROM modeli_genre g "
                              "LEFT JOIN modeli_interestgenre i "
                              "ON g.id = i.genre_id AND i.customer_id =" + str(obj.id))

    user_band = None
    try:
        user_band = Band.objects.get(customer=obj)
    except Band.DoesNotExist:
        pass

    news = None
    try:
        news = BandNews.objects.filter(band=user_band)
    except BandNews.DoesNotExist:
        pass

    if 'band_n' in request.POST:
        name = request.POST['band_n']
        if name == '':
            name = 'all'
        return HttpResponseRedirect(reverse('search_account', args=[name]))

    if 'delete' in request.POST:
        instance = Band.objects.get(customer=obj)
        instance.delete_logo()
        instance.delete_picture()
        for d in news:
            d.delete_picture()
        instance.delete()
        Customer.objects.filter(user=user).update(bend=False)
        return redirect("/account/" + str(code), code)

    if 'logout' in request.POST:
        logout(request)
        return redirect("/login")

    if 'sacuvaj' in request.POST:
        inte = []
        for i in request.POST:
            inte.append(i)
        user_interest = inte[1:-1]

        if user_interest:
            new_interest = []
            for u in user_interest:
                g = Genre.objects.get(id=u)
                new_interest.append(g)
            if user_genre_interest:
                for ugi in user_genre_interest:
                    if ugi.genre in new_interest:
                        new_interest.remove(ugi.genre)
                    else:
                        InterestGenre.objects.filter(customer=obj, genre=ugi.genre).delete()
                for ni in new_interest:
                    InterestGenre.objects.create(customer=obj, genre=ni)
            else:
                for ni in new_interest:
                    InterestGenre.objects.create(customer=obj, genre=ni)
        else:
            InterestGenre.objects.filter(customer=obj).delete()

        return redirect("/account/settings/" + str(code), code)
    """
    content = {
        "title": 'Podešavaje interesovanja',
        "settings": "settings",
        "interests": "interests",
        "account": "account",
        "genre": genre,
    }
    return render(request, "account/personal_interests.html", content)


@login_required(login_url='/account/login/')
def account_search_page(request, name):
    user = request.user
    profile = Profile.objects.get(user=user)
    all_users = User.objects.all()

    # Collecting all user pages
    user_pages = []
    bands = Band.objects.all()
    if bands:
        for b in bands:
            if user == b.creator or user in b.admins.all():
                user_pages.append(b)

    # Checking friend requests
    friend_requests = []
    all_user = Profile.objects.all()
    for u in all_user:
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

    # Checking of data received from search field in navbar and sorting results.
    search_list = []
    order = []
    search = []

    if name == 'all':
        for b in bands:
            search.append(b)
        for u in all_users:
            search.append(u)
    else:
        for u in all_users:
            sequence1 = difflib.SequenceMatcher(isjunk=None, a=u.first_name.lower(), b=name.lower())
            sequence2 = difflib.SequenceMatcher(isjunk=None, a=u.last_name.lower(), b=name.lower())
            difference1 = sequence1.ratio() * 100
            difference1 = round(difference1, 1)
            difference2 = sequence2.ratio() * 100
            difference2 = round(difference2, 1)

            if difference1 > 70:
                search_list.append((u, difference1))
                order = sorted(search_list, key=lambda x: x[1], reverse=True)
            elif difference2 > 70:
                search_list.append((u, difference2))
                order = sorted(search_list, key=lambda x: x[1], reverse=True)
            else:
                pass

        for b in bands:
            sequence_b = difflib.SequenceMatcher(isjunk=None, a=b.name.lower(), b=name.lower())
            difference_b = sequence_b.ratio() * 100
            if difference_b > 49:
                search_list.append((b, difference_b))
                order = sorted(search_list, key=lambda x: x[1], reverse=True)
            else:
                pass

        for o in order:
            search.append(o[0])

    if len(search) == 0:
        search = 'no'

    content = {
        "account": "account",
        "user_search": "user_search",
        "title": 'Demontaža',
        "user": user,
        "profile": profile,
        "user_pages": user_pages,
        "search": search,
        "ime": name,
        "friend_requests": friend_requests,
    }
    return render(request, "account/account_user_search.html", content)
