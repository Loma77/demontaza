from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'help', 'placeholder': 'Ime i prezime',
                                      'oninvalid': "this.setCustomValidity('Molimo vas unesite vaše ime i prezime.')",
                                      'oninput': "setCustomValidity('')",
                                      'required': 'required', 'title': 'Vaše ime i prezime'}), label="Ime i prezime")
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'help', 'placeholder': 'Vaša email adresa',
                                       'oninvalid': "this.setCustomValidity('Molimo vas unesite vašu email adresu.')",
                                       'oninput': "setCustomValidity('')",
                                       'required': 'required', 'title': 'Vaša email adresa'}),
        error_messages={'invalid': 'Email nije u pravilnoj formi.'})
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'help',
                                      'oninvalid': "this.setCustomValidity('Molimo vas unesite temu razgovora.')",
                                      'oninput': "setCustomValidity('')",
                                      'placeholder': 'Tema poruke', 'required': 'required',
                                      'title': 'Molimo vas unesite temu'}), label="Tema poruke")
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'help', 'rows': '4',
                                     'oninvalid': "this.setCustomValidity('Molimo vas unesite objašnjenje.')",
                                     'oninput': "setCustomValidity('')",
                                     'placeholder': 'Tekst poruke', 'required': 'required',
                                     'title': 'Unesite tekst poruke', 'style': 'resize:none; width:100%;'}),
        label="Tekst poruke")


class ContactFormAccount(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'help',
                                      'oninvalid': "this.setCustomValidity('Molimo vas unesite temu razgovora.')",
                                      'oninput': "setCustomValidity('')",
                                      'placeholder': 'Tema poruke', 'required': 'required',
                                      'title': 'Molimo vas unesite temu'}), label="Tema poruke")
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'help', 'rows': '4',
                                     'oninvalid': "this.setCustomValidity('Molimo vas unesite objašnjenje.')",
                                     'oninput': "setCustomValidity('')",
                                     'placeholder': 'Tekst poruke', 'required': 'required',
                                     'title': 'Unesite tekst poruke', 'style': 'resize:none; width:100%;'}),
        label="Tekst poruke")
