from django import forms
from dataentry.models import Pitch, Pitcher, Team, CustomUser

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "team") # Add email to the fields

class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ['team', 'name']

class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = ['team', 'pitcher', 'date', 'pitch_type', 'velo', 'result']
