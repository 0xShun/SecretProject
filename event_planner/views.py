from django.http import JsonResponse
from .models import Event, EventAddress, EventLocation
from accounts.models import UserProfile, UserCredential
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

@require_GET
def event_locations_api(request):
    events = Event.objects.select_related('location').all()
    data = []
    for event in events:
        data.append({
            'event_name': event.event_name,
            'event_date': event.event_date.strftime('%Y-%m-%d %H:%M'),
            'lat': event.location.lat,
            'lng': event.location.long,
            # Add more fields as needed
        })
    return JsonResponse({'events': data})

# Create your views here.
def event_dashboard(request):

    return render(request, 'base.html')

def event_home(request):

    return render(request, 'event_home.html')

def event_events(request):
    user = get_object_or_404(UserProfile, pk=1)
    user_events = Event.objects.filter(event_organizer=user)
    return render(request, 'event_events.html', {'user_events': user_events})


def create_events(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        user = get_object_or_404(UserProfile, pk=1)
        print(user)
        # # Use current user as organizer
        # if not request.user.is_authenticated:
        #     return JsonResponse({'error': 'Unauthorized'}, status=401)

        # # Create location
        location = EventLocation.objects.create(
            lat=data['lat'],
            long=data['long']
        )

        # # Create event
        event = Event.objects.create(
            location=location,
            event_name=data['event_name'],
            event_organizer=user,
            event_date=data['event_date'],
            # status=data['status']
        )

        # # Create address
        EventAddress.objects.create(
            event=event,
            street_address=data['street_address'],
            barangay=data['barangay'],
            city=data['city'],
            country=data['country'],
            zip_code=data['zip_code']
        )

<<<<<<< HEAD
        # return JsonResponse({'message': 'Event created successfully!'})
=======
        return JsonResponse({'message': 'Event created successfully!'})
>>>>>>> 96fa0e8175714b36a4a980aa29a58a214abc6ff3
