from django.contrib import admin

from .models import Pitch, Pitcher, Team, Game, CustomUser


admin.site.register(Pitch)
admin.site.register(Pitcher)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(CustomUser)
