from django.contrib import admin

from .models import Chapter, Page, PageImage, PageTag
# Register your models here.

admin.site.register(Chapter)
admin.site.register(Page)
admin.site.register(PageImage)
admin.site.register(PageTag)