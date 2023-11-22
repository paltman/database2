from django.shortcuts import render, redirect
from dataentry.forms import PitchForm
from dataentry.models import Pitch, Team, Pitcher
from django.db.models import Max

# Imports for registration 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse 
from dataentry.forms import CustomUserCreationForm


# Create your views here.
'''home page'''
def home(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/index.html', context)


'''Settings: Set your date, pitcher, and team'''
def settings(request):
    if request.method == 'POST':
        # Get the team and pitcher instances
        team = Team.objects.get(id=request.POST.get('team'))
        pitcher = Pitcher.objects.get(id=request.POST.get('pitcher'))

        # Set the session variables to the names instead of the ids
        # This is so we can display the names in the entry view
        request.session['team'] = team.name
        request.session['pitcher'] = pitcher.name
        request.session['date'] = request.POST.get('date')

        # Redirect to a page after successfully submitting data
        return redirect('entry')  # Replace 'entry' with your desired URL name

    teams = Team.objects.all()
    pitchers = Pitcher.objects.all()
    # If the request method is not POST (i.e., it's a GET request), render the settings page
    context = {
        'teams': teams,
        'pitchers': pitchers,
        'date': request.session.get('date', ''),
    }
    
    return render(request, 'dataentry/settings.html', context)

'''data adding page'''

def entry(request):
    # Get the pitcher, date_value, and team from the session variables
    pitcher_value = request.session.get('pitcher')
    date_value = request.session.get('date')
    team_value = request.session.get('team')

    # Get the pitcher and team names from the values which pull in ids
    pitcher = Pitcher.objects.get(name=pitcher_value)
    team = Team.objects.get(name=team_value)

    if request.method == 'POST':
        form = PitchForm(request.POST)

        # To allow the pitcher input in the entry view to be a form input as well as a session variable changer
        # Get the pitcher instance
        pitcher = Pitcher.objects.get(id=request.POST.get('pitcher'))
        # Set the session variable to the name instead of the id
        request.session['pitcher'] = pitcher.name

        # Calculate the maximum pitch count for the specified pitcher and date so we know what to add to
        pitch_count = Pitch.objects.filter(pitcher=pitcher, date=date_value, team=team).aggregate(Max('pitch_count'))['pitch_count__max'] or 0

        if form.is_valid():
            # Increment the "Pitch Count" field by 1
            pitch_count += 1
            form.instance.pitch_count = pitch_count
            form.save()
            return redirect('entry')  # Redirect back to the same page
    else:
        # Pre-Populate the form with the date, rest are pre-populated in html
        form = PitchForm(initial={
            'pitcher': pitcher,
            'team': team,
            'date': date_value,
        })

    # Pull in all the data (for that team and that date, for table view.)
    pitchdata = Pitch.objects.filter(team=team, date=date_value)

    # Load in all the data from the Teams and Pitcher models 
        # Pass the available teams and pitchers to the context
    # Limit pitchers to the ones on the selected team
    teams = Team.objects.all()
    pitchers = Pitcher.objects.filter(team=team)

    context = {
        'team_name': team_value,
        'pitcher_name': pitcher_value,
        'pitchdata': pitchdata,
        'form': form,
        'teams': teams,
        'pitchers': pitchers,
    }

    # print(pitcher_value)
    return render(request, 'dataentry/entry.html', context)




'''PowerBI DashBoard'''
def dashboard(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/dashboard.html', context)


'''register user page'''
def register(request):
    # If it's a GET request, we'll just render the form with the context here
    if request.method == 'GET':
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    # If its a POST, a new custom form will be created and the new user will be saved and logged in and redirected to the dashboard
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserCreationForm(request, user)
            return redirect(reverse("dashboard"))


'''my team page'''
def myteam(request):
    # print all the pitchers on the team that the user is associated with
    context = {}
    return render(request, 'dataentry/myteam.html', context)
