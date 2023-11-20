from django.contrib import admin
from dataentry.models import Pitch, Pitcher, Team, Game

# Register your models here.

admin.site.register(Pitch)
admin.site.register(Pitcher)
admin.site.register(Team)
admin.site.register(Game)