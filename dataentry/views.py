from django.shortcuts import render, redirect
from dataentry.forms import PitchingForm
from dataentry.models import PitchingData


# Create your views here.
'''home page'''
def home(request):
    # context is where you can define variables to be used 
    context = {}
    return render(request, 'dataentry/index.html', context)

'''data adding page'''


def submit_data(request):
    pitchdata = PitchingData.objects.all()

    if request.method == 'POST':
        form = PitchingForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            form.save()
            # You can add a success message or other logic here
            return redirect('list_and_submit_pitches')  # Redirect back to the same page

    else:
        form = PitchingForm()  # Create a new form instance for rendering

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

