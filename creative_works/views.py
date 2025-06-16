from django.shortcuts import render

# Create your views here.

def creatives_home(request):

    return render(request, 'creative_home.html')

def upload_book(request):

    return render(request, 'upload_book.html')

def book_page(request):

    return render(request, 'book_page.html')

def book_detail(request, book_id):
    # Placeholder data for now
    book = {
        'title': f'Sample Book Title {book_id}',
        'author': 'Author Name',
        'description': 'This is a placeholder description for the book. In the future, this will be populated with actual book details from the database.',
        'genre': 'Fiction',
        'published_date': '2024'
    }
    return render(request, 'book_detail.html', {'book': book})