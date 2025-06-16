"""
URL configuration for Hackathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
=======
from event_planner import views
>>>>>>> 8eceb3107085b7e26d32d7b65f7f9a9b5efb2583

urlpatterns = [
    path('', views.event_home, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('creative_works/', include('creative_works.urls')),
    path('event_planner/', include('event_planner.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
