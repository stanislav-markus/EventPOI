from django import forms
from registration.forms import RegistrationForm
from django.contrib.sites.models import Site
from core.utils import unique_slugify
from photologue.models import Photo
from core.models import POI, UserProfile


class RegistrationFormWithName(RegistrationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)

    def save(self, commit=True):
        obj = super(PhotoForm, self).save(commit=False)
        unique_slugify(obj, obj.image_filename())
        obj.title = obj.slug
        obj.save()
        obj.sites.add(Site.objects.all()[0])
        return obj


class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)

    def clean(self):
        image = self.cleaned_data.get('image')
        if not image:
            self.cleaned_data['image'] = self.instance.image
        return self.cleaned_data


    def save(self, commit=True):
        obj = super(PhotoUpdateForm, self).save(commit=False)
        unique_slugify(obj, obj.image_filename())
        obj.title = obj.slug
        obj.save()
        obj.sites.add(Site.objects.all()[0])
        return obj


class POIForm(forms.ModelForm):
    class Meta:
        model = POI
        fields = ('name', 'description',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
