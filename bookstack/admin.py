from django.contrib import admin

from .models import (
    Shelve, Book, Chapter, Page, PageReview, Activity
)
# Register your models here.

admin.site.register(Shelve)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Page)
admin.site.register(PageReview)
admin.site.register(Activity)