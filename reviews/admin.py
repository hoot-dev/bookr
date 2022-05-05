from django.contrib import admin

from reviews.models import (
    Book, Publisher, Contributor, BookContributor, Review
)

class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = (
        'title', 'isbn', 'get_publisher', 'publication_date'
    )
    search_fields = ['title', 'publisher__name']

    def get_publisher(self, obj):
        return obj.publisher.name

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    search_fields = ('last_names__startswith', 'first_names')
    list_filter = ('last_names',)

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Linkage', {'fields': ('creator', 'book')}), 
        ('Review content', {'fields': ('content', 'rating')})
    )
    

admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)

