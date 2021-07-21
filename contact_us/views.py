from django.contrib.auth.views import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import ContactForm


# HELP PAGE
def help_page(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            cleaned_form = form.cleaned_data
            subject = f"Pitanje sa Demontaže: {cleaned_form['subject']}"
            message = ""

            html_content = f"<a href='https://www.demontaza.rs/' style='text-decoration: none;'><h2 " \
                           f"style='background-image: linear-gradient(to bottom right, #a6111a,silver 60%); " \
                           f"color:white; text-align:center; padding:5px;'>DEMONTAŽA</h2></a><hr>" \
                           f"Pitanje poslato od: <strong>{cleaned_form['full_name']}</strong> " \
                           f"<br>Email korisnika je: <strong>" \
                           f"{cleaned_form['email']}</strong> i poruka glasi:<br>" \
                           f"<br><i>{cleaned_form['message']}</i>" \
                           f"<hr><a href='https://www.demontaza.rs/' style='text-decoration: none;'>" \
                           f"<p style='text-align:center; color:grey;'><small>&copy; Demontaža 2021" \
                           f"</small></p></a>"

            from_email = "support@demontaza.rs"
            try:
                # ako zelis da posalje html_content, odnosno sa stilovima (bold, italic itd itd)
                msg = EmailMultiAlternatives(subject, message, from_email, ['support@demontaza.rs'])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse("Email hasn't been sent")
            return redirect('success/')
    content = {
        'help_page': 'help_page',
        'title': 'Pomoć',
        'form': form,
        'contact': 'contact'
    }
    return render(request, "contact_us/help_page.html", content)


def help_email_success(request):
    try:
        session_key = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return redirect("/account/home/")
    except:
        pass

    return render(request, "contact_us/help_email_success.html")

