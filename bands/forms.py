from django import forms

from .models import Band


class CreateBand(forms.ModelForm):

    class Meta:
        model = Band
        fields = ['name', 'logo', 'band_picture', 'genre', 'city_or_town', 'year_of_creation', 'members', 'bio',
                  'activity', 'yt_video1', 'yt_video2', 'yt_video3', 'youtube', 'facebook', 'soundcloud', 'instagram',
                  'band_camp']

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
