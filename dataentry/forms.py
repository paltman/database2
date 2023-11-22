from django import forms
from dataentry.models import Pitch, Pitcher, Team

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",) # Add email to the fields

class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ['team', 'name']

class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = ['team', 'pitcher', 'date', 'pitch_type', 'velo', 'result']
