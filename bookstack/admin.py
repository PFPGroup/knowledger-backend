from django.contrib import admin

from .models import (
    Shelve, Book, Chapter, Page, PageReview, Activity, BookViews
)
# Register your models here.

admin.site.index_title = 'مدیریت سایت'
admin.site.site_header = 'ادمین کتابخانه'
admin.site.site_title = 'مدیریت سایت'


class BookStackAdminَArea(admin.AdminSite):
    site_header = 'مدیریت کتابخانه'
bookstack_admin = BookStackAdminَArea(name='BookstackAminArea')


class ShelveAdminModel(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'name', 'jcreated_at', 'is_active')
    list_filter = ('is_active', 'updated_at')
    search_fields = ('creature', 'name', 'description', 'tags')
    exclude = ('slug', 'thumbnail')


class BookAdminModel(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'name', 'creature', 'published')
    list_filter = ('published', 'created_at', 'updated_at')
    search_fields = ('creature', 'name', 'description', 'tags')
    exclude = ('slug', 'thumbnail')


class ChapterAdminModel(admin.ModelAdmin):
    list_display = ('name', 'jcreated_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    exclude = ('slug', 'thumbnail')


class PageAdminModel(admin.ModelAdmin):
    list_display = ('name', 'jcreated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'tags')
    exclude = ('slug', 'thumbnail')


bookstack_admin.register(Shelve, ShelveAdminModel)
bookstack_admin.register(Book, BookAdminModel)
bookstack_admin.register(Chapter, ChapterAdminModel)
bookstack_admin.register(Page, PageAdminModel)

admin.site.register(Page)
admin.site.register(PageReview)
admin.site.register(Activity)
admin.site.register(BookViews)