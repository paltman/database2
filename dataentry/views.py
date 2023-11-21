from django.shortcuts import render, redirect
from dataentry.forms import PitchForm
from dataentry.models import Pitch, Team, Pitcher
from django.db.models import Max


# Create your views here.
'''home page'''
def home(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/index.html', context)


'''Settings: Set your date, pitcher, and team'''
def settings(request):
    if request.method == 'POST':
        # Set the session variables
        request.session['team'] = request.POST.get('team')
        request.session['pitcher'] = request.POST.get('pitcher')
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

    # Calculate the maximum pitch count for the specified pitcher and date.
    pitch_count = Pitch.objects.filter(pitcher=pitcher_value, date=date_value, team=team_value).aggregate(Max('pitch_count'))['pitch_count__max'] or 0

    # Check if the request method is POST
    if request.method == 'POST':
        form = PitchForm(request.POST)
        print("Form data before validation:", form.data)
                # Populate the form with the session variables
        form.initial['team'] = team_value
        form.initial['pitcher'] = pitcher_value
        form.initial['date'] = date_value
        if form.is_valid():
            print('hey')
            # Increment the "Pitch Count" field by 1
            pitch_count += 1
            form.instance.pitch_count = pitch_count

            # Save the form data to the database
            form.save()

            # You can add a success message or other logic here
            return redirect('entry')  # Redirect back to the same page
    else:
        print('form was not validated')
        # Populate the form with the session variables
        form = PitchForm(initial={
            'team': team_value,
            'pitcher': pitcher_value,
            'date': date_value,
        })

    # Pull in all the data (for that team and that date, for table view.)
    pitchdata = Pitch.objects.filter(team=team_value, date=date_value)
    # return the names instead of numbers
    pitcher = Pitcher.objects.get(id=pitcher_value)
    pitcher_name = pitcher.name

    team = Team.objects.get(id=team_value)
    team_name = team.name

    context = {
        'team_name': team_name,
        'pitcher_name': pitcher_name,
        'pitchdata': pitchdata,
        'form': form,
    }

    return render(request, 'dataentry/entry.html', context)




'''PowerBI DashBoard'''
def dashboard(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/dashboard.html', context)

