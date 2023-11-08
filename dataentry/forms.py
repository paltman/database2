from django import forms
from dataentry.models import PitchingData

class PitchingForm(forms.ModelForm):
    # Define choices for pitch_type and result fields
    # It's FB recorded in the database and shown as Fastball for example
    PITCH_TYPE_CHOICES = (
        ('FB', 'Fastball'),
        ('CB', 'Curveball'), 
        ('CH', 'Changeup'), 
    )

    RESULT_CHOICES = (
        ('Hit', 'Hit'),
        ('Ball', 'Ball'),
    )

    PITCHER_CHOICES = {
        ('Joe', 'Joe'),
    }

    # Fields with dropdown lists
    pitch_type = forms.ChoiceField(choices=PITCH_TYPE_CHOICES, widget=forms.Select())
    result = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select())

    class Meta:
        model = PitchingData
        fields = ['team', 'date', 'pitcher', 'pitch_type',
                  'velo', 'result']
