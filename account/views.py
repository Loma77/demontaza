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

from bands.models import Band
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
    # guest_news = News.objects.all().order_by('-updated')

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

        content = {
            "account": "account",
            "user": user,
            "profile": profile,
            "guest_user": guest_user,
            "guest_profile": guest_profile,
        }
        html = render_to_string("account/account_profile_ajax.html", content, request=request)
        return JsonResponse({'form': html})

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
    }
    return render(request, "account/account_settings.html", content)


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
    }
    return render(request, "account/account_user_search.html", content)
