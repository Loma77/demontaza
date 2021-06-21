from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate
from .models import Profile


def get_user(email):
    if email:
        try:
            return User.objects.get(email=email.lower())
        except User.DoesNotExist:
            return None
    else:
        pass


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
                                attrs={
                                    "class": "input-group-field",
                                    "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu email adresu.')",
                                    "oninput": "setCustomValidity('')",
                                    "title": "Molimo vas unesite vašu email adresu.",
                                    "placeholder": "email"
                                }
                            ))
    password = forms.CharField(label='Lozinka',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "input-group-field",
                                       "id": "pswrd",
                                       "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu lozinku.')",
                                       "oninput": "setCustomValidity('')",
                                       "title": "Molimo vas unesite vašu lozinku.",
                                       "placeholder": "Lozinka"
                                   }
                               ))

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        true_mail = self.cleaned_data.get('email')
        qs = User.objects.filter(email=true_mail)
        if qs.exists():
            return true_mail
        else:
            raise forms.ValidationError("Email ne postoji ili je nepravilno unesen.")

    def clean_password(self):
        true_mail = self.cleaned_data.get('email')
        true_password = self.cleaned_data.get('password')
        username = get_user(true_mail)
        user = authenticate(username=username, password=true_password)
        if user:
            return true_password
        else:
            raise forms.ValidationError("Lozinka je netačna.")


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    first_name = forms.CharField(label='Ime',
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "input-group-field",
                                         "oninvalid": "this.setCustomValidity('Molimo vas unesite vaše ime.')",
                                         "oninput": "setCustomValidity('')",
                                         "title": "Molimo vas unesite vaš ime.",
                                         "placeholder": "Ime"
                                     }
                                 ))
    last_name = forms.CharField(label='Prezime',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "input-group-field",
                                        "oninvalid": "this.setCustomValidity('Molimo vas unesite vaše prezime.')",
                                        "oninput": "setCustomValidity('')",
                                        "title": "Molimo vas unesite vaš prezime.",
                                        "placeholder": "Prezime"
                                    }
                                ))
    email = forms.EmailField(widget=forms.EmailInput(
                                attrs={
                                    "class": "input-group-field",
                                    "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu email adresu.')",
                                    "oninput": "setCustomValidity('')",
                                    "title": "Molimo vas unesite vašu email adresu.",
                                    "placeholder": "email"
                                }
                            ))
    password = forms.CharField(label='Lozinka',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "input-group-field",
                                       "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu željenu lozinku.')",
                                       "oninput": "setCustomValidity('')",
                                       "title": "Molimo vas unesite vašu željenu lozinku.",
                                       "placeholder": "Lozinka"
                                   }
                               ))
    password2 = forms.CharField(label='Ponovi lozinku',
                                widget=forms.PasswordInput(
                                    attrs={
                                        "class": "input-group-field",
                                        "oninvalid": "this.setCustomValidity('Molimo vas ponovite lozinku.')",
                                        "oninput": "setCustomValidity('')",
                                        "title": "Molimo vas ponovite lozinku.",
                                        "placeholder": "Ponovi lozinku"
                                    }
                                ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def clean_email(self):
        cd = self.cleaned_data
        qs = User.objects.filter(email=cd['email'])
        if qs.exists():
            raise forms.ValidationError("Ovaj email je već u upotrebi, molimo vas unesite drugi.")
        return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Unesene lozinke nisu iste.')
        return cd['password']


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            return email
        else:
            raise forms.ValidationError("No user.")


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='Ime',
                                 widget=forms.TextInput(
                                     attrs={
                                         "oninvalid": "this.setCustomValidity('Molimo vas unesite vaše ime.')",
                                         "oninput": "setCustomValidity('')",
                                         "title": "Molimo vas unesite vaš ime.",
                                         "placeholder": "Ime"
                                     }
                                 ))
    last_name = forms.CharField(label='Prezime',
                                widget=forms.TextInput(
                                    attrs={
                                        "oninvalid": "this.setCustomValidity('Molimo vas unesite vaše prezime.')",
                                        "oninput": "setCustomValidity('')",
                                        "title": "Molimo vas unesite vaš prezime.",
                                        "placeholder": "Prezime"
                                    }
                                ))
    email = forms.EmailField(widget=forms.EmailInput(
                                attrs={
                                    "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu email adresu.')",
                                    "oninput": "setCustomValidity('')",
                                    "title": "Molimo vas unesite vašu email adresu.",
                                    "placeholder": "email"
                                }
                            ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '42%', "autocomplete": "off",
                                                                     "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu staru lozinku.')",
                                                                     "oninput": "setCustomValidity('')",
                                                                     "title": "Molimo vas unesite vašu staru lozinku.",
                                                                     "placeholder": "Trenutna lozinka"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '42%', "autocomplete": "off",
                                                                      "oninvalid": "this.setCustomValidity('Molimo vas unesite vašu novu lozinku.')",
                                                                      "oninput": "setCustomValidity('')",
                                                                      "title": "Molimo vas unesite vašu novu lozinku.",
                                                                      "placeholder": 'Nova lozinka'}),
                                    help_text="<small style='color:#a6111a;'>"
                                              "<p style='text-align: right; margin-top: -1rem;'>"
                                              "* Vaša lozinka ne sme biti slična ostalim ličnim podacima."
                                              "</p>"
                                              "<p style='text-align: right; margin-top: -1rem;'>"
                                              "* Vaša lozinka mora sadržati najmanje 8 karaktera."
                                              "</p>"
                                              "<p style='text-align: right; margin-top: -1rem;'>"
                                              "* Vaša lozinka ne sme biti često upotrebljavana (test1234...)."
                                              "</p>"
                                              "<p style='text-align: right; margin-top: -1rem;'>"
                                              "* Vaša lozinka ne može biti napravljena samo od brojeva."
                                              "</p></small>",
                                    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '42%', "autocomplete": "off",
                                                                      "oninvalid": "this.setCustomValidity('Molimo vas ponovite vašu novu lozinku.')",
                                                                      "oninput": "setCustomValidity('')",
                                                                      "title": "Molimo vas ponovite vašu novu lozinku.",
                                                                      "placeholder": 'Potvrda nove lozinke'}))

    class Meta:
        model = User

        fields = ['old_password', 'new_password', 'new_password_confirmation']

    def clean_old_password(self):
        cd = self.cleaned_data
        if not self.user.check_password(cd['old_password']):
            raise forms.ValidationError("Ova lozinka nije ispravna.")

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] != cd['new_password2']:
            raise forms.ValidationError("Ponovljena lozinka se razlikuje.")
