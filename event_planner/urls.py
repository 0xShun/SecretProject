from django.urls import path
from . import views


urlpatterns = [
    path('', views.event_dashboard, name='event_dashboard'),
    path('home', views.event_home, name='event_home'),
    path('events', views.event_events, name='event_events'),
    path('events/create', views.create_events, name='create_events'),
    path('events/locations/', views.event_locations_api, name='event_locations_api'),
]
