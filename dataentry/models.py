from django.db import models
from django.utils import timezone

'''Having multiple models in one file allows the project to scale and be more organized.'''

class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)

    # Now, the names of the teams and pitchers will be displayed in the dropdowns instead of their IDs.
    def __str__(self):
        return self.name


class Pitcher(models.Model):
    '''models.CASCADE means that when the referenced Team is deleted, also delete the Pitcher instances that have a foreign key to them.'''
    team = models.ForeignKey(Team, related_name="pitchers", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


# Game is like a pitching session, so this model is where we find the pitch count for each game designed by 'date'
class Game(models.Model):
    team = models.ForeignKey(Team, related_name="games", on_delete=models.CASCADE)
    date = models.DateField()

    def get_pitch_count(self, pitcher):
        return self.pitches.filter(pitcher=pitcher).count()


class PitchType(models.TextChoices):
    FASTBALL = "FB", "Fastball"
    CURVEBALL = "CB", "Curveball"
    CHANGEUP = "CH", "Changeup"
    SLIDER = "SL", "Slider"
    SPLITTER = "SPL", "Splitter"
    CUTTER = "CUT", "Cutter"
    KNUCK = "KN", "Knuck"
    EEPHUS = "EE", "Eephus"


class PitchResult(models.TextChoices):
    BALL = "BALL", "Ball"
    STRIKE_LOOKING = "K Looking", "Strike Looking"
    STRIKE_SWINGING = "K Swinging", "Strike Swinging"
    FOUL = "FB", "Foul Ball"
    BIP_OUT = "BIP OUT", "BIP Out"
    SINGLE = "SGL", "Single"
    DOUBLE = "DBL", "Double"
    TRIPLE = "TPL", "Triple"
    HOMER = "HR", "HR"
    HBP = "HBP", "HBP"
    DROP_3D_SAFE = "D3S", "Drop 3d & Safe"
    REACH_ON_ERROR = "ROE", "Reach on Error"


class Pitch(models.Model):
    """The data for each pitch"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(Pitcher, related_name="pitches", on_delete=models.CASCADE)
    # game = models.ForeignKey(Game, related_name="pitches", on_delete=models.CASCADE)
    date = models.DateField()
    pitch_type = models.CharField(max_length=5, choices=PitchType.choices)
    result = models.CharField(max_length=100, choices=PitchResult.choices)
    pitch_count = models.IntegerField()
    velo = models.DecimalField(max_digits=5, decimal_places=2)
    # timestamp = models.DateTimeField(default=timezone.now)