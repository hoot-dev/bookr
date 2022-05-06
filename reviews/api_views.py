from rest_framework import generics

from .serializers import BookSerializer
from .models import Book


class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer