from django.contrib import admin

from .models import Book, BookImage, Tag
# Register your models here.

admin.site.register(Book)
admin.site.register(BookImage)
admin.site.register(Tag)