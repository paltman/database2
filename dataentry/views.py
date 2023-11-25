from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .forms import PitchForm, CustomUserCreationForm
from .models import Pitch, Team, Pitcher


def home(request):
    """home page"""
    context = {}  # context is where you can define variables to be used
    return render(request, "dataentry/index.html", context)



def settings(request):
    """Settings: Set your date, pitcher, and team"""
    if request.method == "POST":
        # Get the team and pitcher instances to record in the session variables
        team = Team.objects.get(id=request.POST.get("team"))
        pitcher = Pitcher.objects.get(id=request.POST.get("pitcher"))

        # Allow users to set the session variables to the names instead of the ids
        # This is so we can display the names in the entry view
        request.session["team"] = team.name
        request.session["pitcher"] = pitcher.name
        request.session["date"] = request.POST.get("date")

        # Redirect to entry page
        return redirect("entry")

    # Get the logged-in user's team and pitchers
    CustomUser = get_user_model()
    user = CustomUser.objects.get(username=request.user.username)
    teams = Team.objects.filter(id=user.team_id)
    pitchers = Pitcher.objects.filter(team_id=user.team_id)
    # print(user.team_id)
    # print(user.username)
    # If the request method is not POST (i.e., it's a GET request), render the settings page
    context = {
        "teams": teams,
        "pitchers": pitchers,
        "date": request.session.get("date", ""),
        "user": user.username,
    }

    return render(request, "dataentry/settings.html", context)


def entry(request):
    """data adding page"""
    # Get the pitcher, date, and team from the session variables
    pitcher_value = request.session.get("pitcher")
    date_value = request.session.get("date")
    team_value = request.session.get("team")

    # not sure why team_value is being rejected, but adding this extra step fixes it
    team = Team.objects.get(name=team_value)

    if request.method == "POST":
        form = PitchForm(request.POST)

        # To allow the pitcher input in the entry view to be a form input as well as a session variable changer
        # Get the pitcher instance
        pitcher = Pitcher.objects.get(id=request.POST.get("pitcher"))
        # Set the session variable to the name instead of the id
        request.session["pitcher"] = pitcher.name

        # Calculate the maximum pitch count for the specified pitcher and date so we know what to add to
        pitch_count = Pitch.objects.filter(
            pitcher=pitcher,
            date=date_value,
            team=team
        ).aggregate(Max("pitch_count"))["pitch_count__max"] or 0

        if form.is_valid():
            # Increment the "Pitch Count" field by 1
            pitch_count += 1
            form.instance.pitch_count = pitch_count
            form.save()
            return redirect("entry")  # Redirect back to the same page
    else:
        # Pre-Populate the form with the date, rest are pre-populated in html
        form = PitchForm(initial={
            "pitcher": pitcher_value,
            "team": team_value,
            "date": date_value,
        })

    # Pull in all the data (for that team and that date, for table view.)
    pitchdata = Pitch.objects.filter(team=team, date=date_value)

    # Get the logged-in user's team and pitchers
    CustomUser = get_user_model()
    user = CustomUser.objects.get(username=request.user.username)
    teams = Team.objects.filter(id=user.team_id)
    pitchers = Pitcher.objects.filter(team_id=user.team_id)

    context = {
        "team_name": team,
        "pitcher_name": pitcher_value,
        "pitchdata": pitchdata,
        "form": form,
        "teams": teams,
        "pitchers": pitchers,
    }

    # print(pitcher_value)
    return render(request, "dataentry/entry.html", context)


def dashboard(request):
    """PowerBI DashBoard"""
    context = {}  # context is where you can define variables to be used
    return render(request, "dataentry/dashboard.html", context)



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


def myteam(request):
    """my team page"""
    # Fetch the team associated with the logged-in user
    team = request.user.team

    # Fetch all the pitchers associated with that team
    pitchers = Pitcher.objects.filter(team=team)

    # Pass the pitchers to the context
    context = {
        "team": team,
        "pitchers": pitchers
        }

    return render(request, "dataentry/myteam.html", context)
