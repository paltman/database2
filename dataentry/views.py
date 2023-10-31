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

'''data adding page'''

def submit_data(request):
    # Query the most recent entry in the database
    latest_entry = PitchingData.objects.latest('date')
    # Extract pitcher and date from the form data
    pitcher = request.POST.get('pitcher')
    date = request.POST.get('date')

    # Calculate the maximum pitch count for the specified pitcher and date
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT MAX(pitch_count) FROM dataentry_pitchingdata
            WHERE pitcher = %s AND date = %s
            """,
            [pitcher, date]
        )
        latest_pitch_count = cursor.fetchone()[0] or 0

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

    # Store all data
    pitchdata = PitchingData.objects.all()

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

