from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import Pitch, Pitcher, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "team")  # Add email to the fields


class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ["team", "name"]


class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = ["team", "pitcher", "date", "pitch_type", "velo", "result"]
