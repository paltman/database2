from django.db import models

from django.contrib.auth.models import AbstractUser


# Needed to update settings for this one
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    team = models.ForeignKey("dataentry.Team", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
