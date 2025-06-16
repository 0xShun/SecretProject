from django.urls import path
from . import views



urlpatterns = [
    path('', views.creatives_home, name='creatives_home'),
    path('upload_book', views.upload_book, name='upload_book'),
    path('book_page', views.book_page, name='book_page'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
]
