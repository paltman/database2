from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm

from .forms import CustomUserCreationForm


def register(request):
    """register user page"""
    # If it's a GET request, we'll just render the form with the context here
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    # If its a POST, a new custom form will be created and the new user will be saved and logged in
    # and redirected to the dashboard
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            CustomUser = form.save()
            UserCreationForm(request, CustomUser)
            return redirect(reverse("login"))
