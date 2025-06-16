from django.urls import path
from . import views

urlpatterns = [   
    path('profile/', views.index, name="profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('register/', views.register, name="register"),
    path('verify/', views.verify_code, name="verify_code"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-password-reset/', views.verify_password_reset, name='verify_password_reset'),
]
