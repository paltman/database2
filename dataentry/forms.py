from django import forms
from dataentry.models import Pitch, Pitcher, Team

class PitcherForm(forms.ModelForm):
    class Meta:
        model = Pitcher
        fields = ['team', 'name']

class PitchForm(forms.ModelForm):
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
        ('Drop 3rd & Safe', 'Drop 3rd & Safe'),
    )

    # This function allows the dropdown lists to be dynamic for team and pitcher.
    #    if team is selected as a session variable, then the pitcher dropdown list will be filtered by the team
    def __init__(self, *args, **kwargs):
        super(PitchForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.all()
        if 'team' in self.data:
            try:
                team_id = int(self.data.get('team'))
                self.fields['pitcher'].queryset = Pitcher.objects.filter(team_id=team_id).all()
            except (ValueError, TypeError):
                pass  # if invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['pitcher'].queryset = self.instance.team.pitcher_set.all()


    # Fields with dropdown lists
    pitcher = forms.ModelChoiceField(queryset=Pitcher.objects.all())
    pitch_type = forms.ChoiceField(choices=PITCH_TYPE_CHOICES, widget=forms.Select())
    result = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select())

    class Meta:
        model = Pitch
        fields = ['pitcher', 'team', 'date', 'pitch_type',
                  'velo', 'result']
