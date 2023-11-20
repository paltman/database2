from django.db import models
from django.utils import timezone

'''Having multiple models in one file allows the project to scale and be more organized.'''

class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Pitcher(models.Model):
    '''models.CASCADE means that when the referenced Team is deleted, also delete the Pitcher instances that have a foreign key to them.'''
    team = models.ForeignKey(Team, related_name="pitchers", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)


# Game is like a pitching session, so this model is where we find the pitch count for each game designed by 'date'
class Game(models.Model):
    team = models.ForeignKey(Team, related_name="games", on_delete=models.CASCADE)
    date = models.DateField()

    def get_pitch_count(self, pitcher):
        return self.pitches.filter(pitcher=pitcher).count()


class PitchKind(models.TextChoices):
    FASTBALL = "FB", "Fastball"
    CURVEBALL = "CB", "Curveball"
    CHANGEUP = "CH", "Changeup"
    SLIDER = "SL", "Slider"
    SPLITTER = "SP", "Splitter"
    CUTTER = "CU", "Cutter"
    KNUCK = "KN", "Knuck"
    EEPHUS = "EE", "Eephus"


class PitchResult(models.TextChoices):
    BALL = "BL", "Ball"
    STRIKE_LOOKING = "XL", "Strike Looking"
    STRIKE_SWINGING = "XS", "Strike Swinging"
    FOUL = "FB", "Foul Ball"
    BIP_OUT = "BO", "BIP Out"
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
    game = models.ForeignKey(Game, related_name="pitches", on_delete=models.CASCADE)
    date = models.DateField()
    kind = models.CharField(max_length=5, choices=PitchKind.choices)
    result = models.CharField(max_length=100, choices=PitchResult.choices)
    pitch_count = models.IntegerField()
    velo = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
