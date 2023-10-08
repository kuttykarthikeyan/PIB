from django import forms

from .models import Eprints

class Eprintsform(forms.ModelForm):

    class Meta:
        model = Eprints
        fields = '__all__'

