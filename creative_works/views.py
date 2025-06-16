from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookUploadForm

# Create your views here.

def creatives_home(request):

    return render(request, 'creative_home.html')

def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploader = request.user.userprofile  # Assuming you have user authentication set up
            book.save()
            messages.success(request, 'Book uploaded successfully!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookUploadForm()
    
    return render(request, 'upload_book.html', {'form': form})

def book_page(request):

    return render(request, 'book_page.html')

def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        # Placeholder data for now
        book = {
            'title': f'Sample Book Title {book_id}',
            'author': 'Author Name',
            'description': 'This is a placeholder description for the book. In the future, this will be populated with actual book details from the database.',
            'genre': 'Fiction',
            'published_date': '2024'
        }
    return render(request, 'book_detail.html', {'book': book})