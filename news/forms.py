from django import forms
import requests

from .models import News


class CreateNews(forms.ModelForm):
    title = forms.CharField(required=False, label='Naslov',
                            widget=forms.TextInput(
                                attrs={
                                    "class": "form-cotrol",
                                    "title": "Naslov objave ili događaja.",
                                    "placeholder": "Naslov objave ili događaja"
                                }
                            ))
    yt_video = forms.CharField(required=False, label='YouTube link',
                               widget=forms.TextInput(
                                   attrs={
                                       "class": "form-cotrol",
                                       "title": "YouTube link objave ili događaja.",
                                       "placeholder": "YouTube link"
                                   }
                               ))
    fb_event = forms.CharField(required=False, label='Facebook događaj',
                               widget=forms.TextInput(
                                   attrs={
                                       "class": "form-cotrol",
                                       "title": "Facebook link objave ili događaja.",
                                       "placeholder": "Facebook događaj"
                                   }
                               ))

    class Meta:
        model = News
        fields = ['title', 'news', 'news_picture', 'yt_video', 'fb_event']

    def clean_yt_video(self, *args, **kwargs):
        yt_video_raw = self.cleaned_data.get('yt_video')

        video = "https://www.youtube.com/watch?v="
        video_verify = "https://www.youtube.com/embed/"

        if yt_video_raw:
            try:
                response = requests.get(yt_video_raw)
                yt_video = response.url
                yt_video = yt_video.replace("&feature=youtu.be", "")

                if yt_video:
                    if video_verify in yt_video:
                        return yt_video
                    elif video not in yt_video:
                        yt_video = None
                        return yt_video
                    else:
                        yt_video = yt_video.replace("https://www.youtube.com/watch?v=",
                                                    "https://www.youtube.com/embed/")
                        return yt_video
            except:
                raise forms.ValidationError('Niste uneli ispravan YouTube link.')

    def clean_fb_event(self, *args, **kwargs):
        fb_event = self.cleaned_data.get('fb_event')

        face = "https://www.facebook.com/"

        if fb_event:
            if face in fb_event:
                return fb_event
            else:
                raise forms.ValidationError('Niste uneli ispravan Facebook link.')

    def clean(self, *args, **kwargs):
        news_title = self.cleaned_data.get('title')
        news_text = self.cleaned_data.get('news')
        news_picture = self.cleaned_data.get('news_picture')
        yt_video = self.cleaned_data.get('yt_video')
        fb_event = self.cleaned_data.get('fb_event')

        if news_title == '' and news_text == '' and news_picture is None and yt_video is None and fb_event is None:
            raise forms.ValidationError("Ne možete odjaviti vest bez bar jednog unetog podatka.")


class NewsPictureForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['news_picture']
