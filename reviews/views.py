from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.core.files.images import ImageFile

from .models import Book, Contributor, Publisher, Review
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from .utils import average_rating

from io import BytesIO
from PIL import Image



def index(request):
    return render(request, 'base.html')

@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book
        if review is None:
            messages.success(request, 'Review for "{}" was created.'.format(book))
        else:
            updated_review.date_edited = timezone.now()
            messages.success(request, 'Review for "{}" was updated.'.format(book))
        
        updated_review.save()

        return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'model_type': 'Review',
        'related_instance': book,
        'related_model_type': 'Book',
        'form': form,
        'instance': review
    }
    return render(request, 'reviews/instance-form.html', context)

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
        if publisher is None:
            messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
        else:
            messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

        return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    context = {
        'model_type': 'Publisher',
        'form': form,
        'instance': publisher
    }
    return render(request, 'reviews/instance-form.html', context)


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            lname_contributors = Contributor.objects.filter(last_names__icontains=search)

            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "books": books})


def book_list(request):
    books = Book.objects.all()
    book_list = []

    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({
            'book': book,
            'book_rating': book_rating,
            'number_of_reviews': number_of_reviews
        })
        context = {
            'book_list': book_list
        }
    return render(request, 'reviews/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()

    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
    else:
        book_rating = None

    context = {
        'book': book,
        'book_rating': book_rating,
        'reviews': reviews
    }

    return render(request, 'reviews/book_detail.html', context)


@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookMediaForm(request.POST, request.FILES, instance=book)
    
        if form.is_valid():
            book = form.save(False)
            cover = form.cleaned_data.get("cover")
            if cover:
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, "Book '{}' was successfully updated.".format(book))
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)
    
    context = {
        "instance": book,
        "form": form,
        "model_type": "Book",
        "is_file_upload": True
    }
    
    return render(request, "reviews/instance-form.html", context)
    