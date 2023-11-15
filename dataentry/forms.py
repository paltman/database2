from django import forms
from dataentry.models import PitchingData

class PitchingForm(forms.ModelForm):
    # Define choices for pitch_type and result fields
    # It's FB recorded in the database and shown as Fastball for example
    PITCH_TYPE_CHOICES = (
        ('FB', 'Fastball'),
        ('CB', 'Curveball'), 
        ('CH', 'Changeup'),
        ('SL', 'Slider'),
        ('Splitter', 'Splitter'),
        ('Cutter', 'Cutter'),
        ('Knuck', 'Knuck'),
        ('EEPHUS', 'Eephus'),
    )
    # Calculate data in the background like when there is a strikeout or a walk
    RESULT_CHOICES = (
        ('Ball', 'Ball'),
        ('Strike Looking', 'Strike Looking'),
        ('Strike Swinging', 'Strike Swinging'),
        ('Foul Ball', 'Foul Ball'),
        ('BIP Out', 'BIP Out'),
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
        ('HR', 'HR'),
        ('HBP', 'HBP'),
        ('Drop 3rd & Safe', 'Drop 3d & Safe'),
    )

    PITCHER_CHOICES = (
        ('Joe', 'Joe'),
        ('Candice', 'Candice'),
        ('Argo', 'Argo'),
        ('Joe', 'Joe'),
    )

    TEAM_CHOICES = (
        ('Bloom', 'Bloom'),
        ('Suncoast', 'Suncoast'),
        ('Richmond', 'Richmond'),
    )

    # Fields with dropdown lists
    pitch_type = forms.ChoiceField(choices=PITCH_TYPE_CHOICES, widget=forms.Select())
    result = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select())
    pitcher = forms.ChoiceField(choices=PITCHER_CHOICES, widget=forms.Select())
    team = forms.ChoiceField(choices=TEAM_CHOICES, widget=forms.Select())

    class Meta:
        model = PitchingData
        fields = ['team', 'date', 'pitcher', 'pitch_type',
                  'velo', 'result']
