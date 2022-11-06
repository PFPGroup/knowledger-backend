from django.contrib import admin
from .models import (
    Shelve, Book, Tag
)

# Register your models here.

admin.site.register(Shelve)
admin.site.register(Book)
admin.site.register(Tag)