from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from taggit.serializers import (TaggitSerializer, TagListSerializerField)

from bookstack.models import Page, PageReview, Book

class PageReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageReview
        fields = ('user', 'text', 'created_at')


class PageSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    reviews = PageReviewSerializer
    
    class Meta:
        model = Page
        fields = ('name', 'text', 'created_at', 'updated_at', 'tags', 'reviews')


class UpdateCreatePageSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Page
        fields = ('name', 'text', 'tags')
    
    def create(self, validated_data):
        book = get_object_or_404(Book, slug=self.context['book_slug'])
        if self.context['request'].user in book.authors.all():
            validated_data['chapter'] = book
            return super().create(validated_data)
        else:
            raise serializers.ValidationError(
                {'permission': 'you have no permissions to this action'}
            )
    
    def update(self, instance, validated_data):
        book = get_object_or_404(Book, slug=self.context['book_slug'])
        if self.context['request'].user in book.authors.all():
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {'permission': 'you have no permissions to this action'}
            )