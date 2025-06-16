from django.http import JsonResponse
from .models import Event, EventAddress, EventLocation
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import render

# Create your views here.
def event_dashboard(request):

    return render(request, 'event_base.html')

def event_home(request):

    return render(request, 'event_home.html')

def event_events(request):

    return render(request, 'event_events.html')


def create_events(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        # # Use current user as organizer
        # if not request.user.is_authenticated:
        #     return JsonResponse({'error': 'Unauthorized'}, status=401)

        # # Create location
        # location = EventLocation.objects.create(
        #     lat=data['lat'],
        #     long=data['long']
        # )

        # # Create event
        # event = Event.objects.create(
        #     location=location,
        #     event_name=data['event_name'],
        #     event_organizer=request.user,
        #     event_date=data['event_date'],
        #     status=data['status']
        # )

        # # Create address
        # EventAddress.objects.create(
        #     event=event,
        #     street_address=data['street_address'],
        #     barangay=data['barangay'],
        #     city=data['city'],
        #     country=data['country'],
        #     zip_code=data['zip_code']
        # )

        # return JsonResponse({'message': 'Event created successfully!'})