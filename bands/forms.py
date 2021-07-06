from django import forms
import requests

from .models import Band


class CreateBand(forms.ModelForm):
    video = "https://www.youtube.com/watch?v="
    video_verify = "https://www.youtube.com/embed/"
    channel = "https://www.youtube.com/channel/"
    face = "https://www.facebook.com/"
    sound = "https://soundcloud.com/"
    instag = "https://www.instagram.com/"

    name = forms.CharField(label='Ime benda',
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "title": "Ime benda",
                                   "placeholder": "Ime benda",
                                   "oninvalid": "this.setCustomValidity('Molimo vas unesite ime benda.')",
                                   "oninput": "setCustomValidity('')"
                               }
                           ))
    year_of_creation = forms.CharField(label='Godina nastanka',
                                       widget=forms.TextInput(
                                           attrs={
                                               "class": "form-control",
                                               "type": "number",
                                               "title": "Godina nastanka benda",
                                               "placeholder": "Godina nastanka benda",
                                               "oninvalid": "this.setCustomValidity('Molimo vas unesite samo godinu brojevima.')",
                                               "oninput": "setCustomValidity('')"
                                           }
                                       ))
    yt_video1 = forms.CharField(required=False, label='YT link',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "type": "text",
                                    }
                                ))
    yt_video2 = forms.CharField(required=False, label='YT link',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "type": "text",
                                    }
                                ))
    yt_video3 = forms.CharField(required=False, label='YT link',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "type": "text",
                                    }
                                ))
    youtube = forms.CharField(required=False, label='YT link',
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "text",
                                  }
                              ))
    facebook = forms.CharField(required=False, label='YT link',
                               widget=forms.TextInput(
                                   attrs={
                                       "class": "form-control",
                                       "type": "text",
                                   }
                               ))
    soundcloud = forms.CharField(required=False, label='YT link',
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    instagram = forms.CharField(required=False, label='YT link',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "type": "text",
                                    }
                                ))
    band_camp = forms.CharField(required=False, label='YT link',
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "type": "text",
                                    }
                                ))

    class Meta:
        model = Band
        fields = ['name', 'logo', 'band_picture', 'genre', 'city_or_town', 'year_of_creation', 'members', 'bio',
                  'activity', 'yt_video1', 'yt_video2', 'yt_video3', 'youtube', 'facebook', 'soundcloud', 'instagram',
                  'band_camp']

    def clean_yt_video1(self, *args, **kwargs):
        yt_video_raw = self.cleaned_data.get('yt_video1')

        if yt_video_raw:
            try:
                response = requests.get(yt_video_raw)
                yt_video1 = response.url
                yt_video1 = yt_video1.replace("&feature=youtu.be", "")

                if yt_video1:
                    if self.video_verify in yt_video1:
                        return yt_video1
                    elif self.video not in yt_video1:
                        yt_video1 = None
                        return yt_video1
                    else:
                        yt_video1 = yt_video1.replace("https://www.youtube.com/watch?v=",
                                                      "https://www.youtube.com/embed/")
                        return yt_video1
            except:
                raise forms.ValidationError('Niste uneli ispravan YouTube link.')

    def clean_yt_video2(self, *args, **kwargs):
        yt_video_raw = self.cleaned_data.get('yt_video2')

        if yt_video_raw:
            try:
                response = requests.get(yt_video_raw)
                yt_video2 = response.url
                yt_video2 = yt_video2.replace("&feature=youtu.be", "")

                if yt_video2:
                    if self.video_verify in yt_video2:
                        return yt_video2
                    elif self.video not in yt_video2:
                        yt_video2 = None
                        return yt_video2
                    else:
                        yt_video2 = yt_video2.replace("https://www.youtube.com/watch?v=",
                                                      "https://www.youtube.com/embed/")
                        return yt_video2
            except:
                raise forms.ValidationError('Niste uneli ispravan YouTube link.')

    def clean_yt_video3(self, *args, **kwargs):
        yt_video_raw = self.cleaned_data.get('yt_video3')

        if yt_video_raw:
            try:
                response = requests.get(yt_video_raw)
                yt_video3 = response.url
                yt_video3 = yt_video3.replace("&feature=youtu.be", "")

                if yt_video3:
                    if self.video_verify in yt_video3:
                        return yt_video3
                    elif self.video not in yt_video3:
                        yt_video3 = None
                        return yt_video3
                    else:
                        yt_video3 = yt_video3.replace("https://www.youtube.com/watch?v=",
                                                      "https://www.youtube.com/embed/")
                        return yt_video3
            except:
                raise forms.ValidationError('Niste uneli ispravan YouTube link.')

    def clean_youtube(self, *args, **kwargs):
        youtube = self.cleaned_data.get('youtube')

        if youtube:
            if self.channel in youtube:
                return youtube
            else:
                raise forms.ValidationError('Niste uneli ispravan link ka YouTube kanalu.')

    def clean_facebook(self, *args, **kwargs):
        facebook = self.cleaned_data.get('facebook')

        if facebook:
            if self.face in facebook:
                return facebook
            else:
                raise forms.ValidationError('Niste uneli ispravan link ka Facebook strani.')

    def clean_soundcloud(self, *args, **kwargs):
        soundcloud = self.cleaned_data.get('soundcloud')

        if soundcloud:
            if self.sound in soundcloud:
                return soundcloud
            else:
                raise forms.ValidationError('Niste uneli ispravan link ka Soundcloud profilu.')

    def clean_instagram(self, *args, **kwargs):
        instagram = self.cleaned_data.get('instagram')

        if instagram:
            if self.instag in instagram:
                return instagram
            else:
                raise forms.ValidationError('Niste uneli ispravan link ka Instagram strani.')

    def clean_band_camp(self, *args, **kwargs):
        band_camp = self.cleaned_data.get('band_camp')

        if band_camp:
            if '.bandcamp.com' in band_camp:
                return band_camp
            else:
                raise forms.ValidationError('Niste uneli ispravan link ka Band Camp profilu.')

    def clean(self, *args, **kwargs):
        band_name = self.cleaned_data.get('name')
        city_or_town = self.cleaned_data.get('city_or_town')
        qs = Band.objects.filter(name=band_name, city_or_town=city_or_town)
        if qs.exists():
            raise forms.ValidationError("Bend sa ovim imenom i lokacijom, već postoji u bazi podataka.")


class EditBand(forms.ModelForm):

    class Meta:
        model = Band
        fields = ['name', 'logo', 'band_picture', 'genre', 'city_or_town', 'year_of_creation', 'members', 'bio',
                  'activity', 'yt_video1', 'yt_video2', 'yt_video3', 'youtube', 'facebook', 'soundcloud', 'instagram',
                  'band_camp']

    def clean(self, *args, **kwargs):
        instance = self.instance
        name = self.cleaned_data.get('name')
        city_or_town = self.cleaned_data.get('city_or_town')
        qs = Band.objects.filter(name=name, city_or_town=city_or_town)
        if instance is not None:
            qs = qs.exclude(creator=instance.creator)
        if qs.exists():
            raise forms.ValidationError("Bend sa ovim imenom i lokacijom, već postoji u bazi podataka.")


class BandLogoForm(forms.ModelForm):

    class Meta:
        model = Band
        fields = ['logo']


class BandPictureForm(forms.ModelForm):

    class Meta:
        model = Band
        fields = ['band_picture']
