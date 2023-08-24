from django import forms 
from django.forms import ModelForm
from .models import User, MediaFile


class MediaFileForm(ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'