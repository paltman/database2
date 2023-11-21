from django import forms
from dataentry.models import Pitch, Pitcher, Team

class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ['team', 'name']

class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = ['team', 'pitcher', 'date', 'pitch_type', 'velo', 'result']
