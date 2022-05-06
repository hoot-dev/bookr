from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('api/all_books/', api_views.AllBooks.as_view(), name='all_books'),
    path('api/contributors/', api_views.ContributorView.as_view(), name='contributors'),
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>', views.book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>', views.review_edit, name='review_edit'),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('book-search/', views.book_search, name='book_search'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
]