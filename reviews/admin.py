from django.contrib import admin

from reviews.models import (
    Book, Publisher, Contributor, BookContributor, Review
)

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Contributor)
admin.site.register(BookContributor)
admin.site.register(Review)
