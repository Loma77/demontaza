from django import forms

from .models import News


class CreateNews(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title', 'news', 'news_picture', 'yt_video', 'fb_event']

    def clean(self, *args, **kwargs):
        news_title = self.cleaned_data.get('title')
        news_text = self.cleaned_data.get('news')
        news_picture = self.cleaned_data.get('news_picture')
        yt_video = self.cleaned_data.get('yt_video')
        fb_event = self.cleaned_data.get('fb_event')

        if news_title is None and news_text is None and news_picture is None and yt_video is None and fb_event is None:
            raise forms.ValidationError("Ne možete odjaviti vest bez bar jednog podatka.")

