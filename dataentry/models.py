from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Pitcher(models.Model):
    team = models.ForeignKey(Team, related_name="pitchers")
    name = models.CharField(max_length=150, unique=True)


class Game(models.Model):
    team = models.ForeignKey(Team, related_name="games")
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


class Pitch(models.Model):
    """The data for each pitch"""
    pitcher = models.ForeignKey(Pitcher, related_name="pitches")
    game = models.ForeignKey(Game, related_name="pitches")
    kind = models.CharField(length=2, choices=PitchKind.choices)
    result = models.CharField(length=1, choices=PitchResult.choices)
    velo = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
