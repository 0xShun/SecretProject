from django.shortcuts import render

# Create your views here.

def creatives_home(request):

    return render(request, 'creative_home.html')

def upload_book(request):

    return render(request, 'upload_book.html')

def book_page(request):

    return render(request, 'book_page.html')