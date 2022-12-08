from rest_framework import serializers
from django.shortcuts import get_object_or_404

from bookstack.models import Chapter, Page, Book


class ChapterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'description', 'created_at',)


class ChapterPagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page
        fields = ('slug', 'name',)


class ChapterDetailSerializer(serializers.ModelSerializer):
    page = ChapterPagesSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'description', 'created_at', 'page',)


class CreateUpdateChapterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chapter
        fields = ('name', 'description', )
    
    def create(self, validated_data):
        book = get_object_or_404(Book, slug=self.context['book_slug'])
        validated_data['book'] = book
        return super().create(validated_data)