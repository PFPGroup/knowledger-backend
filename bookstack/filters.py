from django_filters.rest_framework import FilterSet

from bookstack.models import Shelve, Book, Chapter, Page


class ShelveFilterset(FilterSet):

    class Meta:
        model = Shelve
        fields = {
            'updated_at': ['gt','lt'],
            'created_at': ['gt', 'lt'],
        }


class BookFilterset(FilterSet):

    class Meta:
        model = Book
        fields = {
            'updated_at': ['gt','lt'],
            'created_at': ['gt', 'lt'],
        }


class ChapterFilterset(FilterSet):

    class Meta:
        model = Chapter
        fields = {
            'created_at': ['gt', 'lt'],
        }


class PageFilterset(FilterSet):

    class Meta:
        model = Page
        fields = {
            'updated_at': ['gt','lt'],
            'created_at': ['gt', 'lt'],
        }