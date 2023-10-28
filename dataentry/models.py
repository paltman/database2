from django.db import models

# Create your models here.

'''PitchingData to capture inputs'''
class PitchingData(models.Model):
    team = models.CharField(max_length=100)
    date = models.DateField()
    # add in pitcher_choices from a database table of teams and their pitchers
    pitcher = models.CharField(max_length=50)
    # ensures variable is a non negative integer
    pitch_count = models.PositiveIntegerField()
    # add in pitch_type_choices
    pitch_type = models.CharField(max_length=50)
    velo = models.DecimalField(max_digits=5, decimal_places=2)
    # add in result_choices
    result = models.CharField(max_length=100) 

'''TeamData: will be a form on home page for teams to add all their pitchers and team name and stuff like that'''
