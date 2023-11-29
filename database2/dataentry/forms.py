from django import forms

from .models import Pitch, Pitcher


class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ["team", "name"]


class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = ["team", "pitcher", "date", "pitch_type", "velo", "result"]
