from django.shortcuts import render, redirect
from dataentry.forms import PitchingForm
from dataentry.models import PitchingData
from django.db import connection


# Create your views here.
'''home page'''
def home(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/index.html', context)


'''Settings: Set your date, pitcher, and team'''
def settings(request):
    if request.method == 'POST':
        # Get the data from the first form
        team = request.POST.get('team')
        pitcher = request.POST.get('pitcher')
        date_value = request.POST.get('date')

        # Create a new PitchData instance with the provided data and "NA" for other fields
        pitch_data = PitchingData(team=team, pitcher=pitcher, date=date_value, pitch_count=0, pitch_type=" ", velo=0, result=" ")
        pitch_data.save()  # Save the data to the database

        # Redirect to a page after successfully submitting data
        return redirect('submit_data')  # Replace 'success_page' with your desired URL name
    return render(request, 'dataentry/settings.html')

'''data adding page'''

def submit_data(request):
    # Query the most recent entry in the database. We will use this to auto fill the input values for Team, Date, and Pitcher
    latest_entry = PitchingData.objects.latest('id')
    # Extract pitcher and date from the form data. We will use this to Query the dataset and auto count pitches 
    #    based on how pitchers on that specific day. So when you change pitchers or Joe pitches on another day the pitch counter resets
    pitcher = request.POST.get('pitcher')
    date_value = request.POST.get('date')
    team = request.POST.get('team')

    # Calculate the maximum pitch count for the specified pitcher and date. This is where we get the latest pitch count!!!
    #    %s = the input
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT MAX(pitch_count) FROM dataentry_pitchingdata
            WHERE pitcher = %s AND date = %s AND team = %s
            """,
            [pitcher, date_value, team]
        )
        latest_pitch_count = cursor.fetchone()[0] or 0

    # So, once we hit submit, submit the form and check the data types are valid. Then add 1 as the input for pitch count and save to 
    #     database
    # else : so after this, assign the values that we want auto assigned in the input boxes.
    if request.method == 'POST':
        form = PitchingForm(request.POST)

        if form.is_valid():
            # Increment the "Pitch Count" field by 1
            latest_pitch_count += 1
            form.instance.pitch_count = latest_pitch_count

            # Save the form data to the database
            form.save()

            # You can add a success message or other logic here
            return redirect('submit_data')  # Redirect back to the same page
    else:
          # Format the date explicitly
        date_value = latest_entry.date.strftime('%Y-%m-%d') if latest_entry else None

        # Populate the form with the most recent values
        form = PitchingForm(initial={
            'team': latest_entry.team if latest_entry else '',
            'pitcher': latest_entry.pitcher if latest_entry else '',
            'date': date_value,
            })

    # Pull in all the data (for that team and that date, for table view.)
    pitchdata = PitchingData.objects.filter(team=latest_entry.team, date=date_value, pitch_type__gt=" ")  # Filter for non-empty 'Pitch Type')

    context = {
        'pitchdata': pitchdata,
        'form': form,
    }

    return render(request, 'dataentry/entry.html', context)



'''PowerBI DashBoard'''
def dashboard(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/dashboard.html', context)

