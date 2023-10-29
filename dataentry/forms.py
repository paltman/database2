from django import forms
from dataentry.models import PitchingData

class PitchingForm(forms.ModelForm):
    class Meta:
        model = PitchingData
        fields = ['team', 'date', 'pitcher', 'pitch_count', 'pitch_type',
                  'velo', 'result']
