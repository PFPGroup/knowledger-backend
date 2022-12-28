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


def make_publish(modeladmin, request, queryset):
    rows_updated = queryset.update(published=True)
    if rows_updated == 1:
        message_bit = 'منتشر شد'
    else:
        message_bit = 'منتشر شدند'
    modeladmin.message_user(request, f'{rows_updated} کتاب {message_bit}')
make_publish.short_description = 'انتشار کتاب های انتخاب شده'

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(published=False)
    if rows_updated == 1:
        message_bit = 'پیش نویس شد'
    else:
        message_bit = 'پیش نویس شدند'
    modeladmin.message_user(request, f'{rows_updated} کتاب {message_bit}')
make_draft.short_description = 'پیش نویس کردن کتاب های انتخاب شده'

def make_active(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active=True)
    if rows_updated == 1:
        message_bit = 'فعال شد'
    else:
        message_bit = 'فعال شدند'
    modeladmin.message_user(request, f'{rows_updated} قفسه {message_bit}')
make_active.short_description = 'فعال کردن قفسه ها انتخاب شده'

def make_unactive(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active=False)
    if rows_updated == 1:
        message_bit = 'غیره فعال شد'
    else:
        message_bit = 'غیره فعال شدند'
    modeladmin.message_user(request, f'{rows_updated} قفسه {message_bit}')
make_unactive.short_description = 'غیره فعال کردن قفسه های انتخاب شده'


class ShelveAdminModel(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'name', 'jcreated_at', 'is_active')
    list_filter = ('is_active', 'updated_at')
    search_fields = ('creature', 'name', 'description', 'tags')
    exclude = ('slug', 'thumbnail')
    actions = (make_active, make_unactive)


class BookAdminModel(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'name', 'creature', 'published')
    list_filter = ('published', 'created_at', 'updated_at')
    search_fields = ('creature', 'name', 'description', 'tags')
    exclude = ('slug', 'thumbnail')
    actions = (make_publish, make_draft)



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

bookstack_admin.disable_action('delete_selected')

bookstack_admin.register(Shelve, ShelveAdminModel)
bookstack_admin.register(Book, BookAdminModel)
bookstack_admin.register(Chapter, ChapterAdminModel)
bookstack_admin.register(Page, PageAdminModel)

admin.site.register(Page)
admin.site.register(PageReview)
admin.site.register(Activity)
admin.site.register(BookViews)