from rest_framework import serializers

from .models import Publisher, Book, BookContributor, Contributor

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'website', 'email']


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'publisher']

class ContributionSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ['book', 'role']

class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set = ContributionSerializer(read_only=True, many=True)
    number_contributions = serializers.IntegerField(read_only=True)
    initialled_name = serializers.CharField(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'initialled_name', 
            'email', 
            'bookcontributor_set', 
            'number_contributions'
        ]