from django.contrib import admin

from reviews.models import (
    Book, Publisher, Contributor, BookContributor, Review
)

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13')
    list_filter = ('publisher', 'publication_date')
    search_fields = ('title', 'isbn', 'publisher__name')

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

