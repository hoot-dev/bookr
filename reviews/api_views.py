from rest_framework import generics

from .serializers import BookSerializer, ContributorSerializer
from .models import Book, Contributor


class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ContributorView(generics.ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer