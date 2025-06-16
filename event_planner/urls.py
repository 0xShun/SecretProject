from django.urls import path
from . import views


urlpatterns = [
    path('', views.event_dashboard, name='event_dashboard'),
    path('home', views.event_home, name='event_home'),
]
