from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from taggit.serializers import (TaggitSerializer, TagListSerializerField)

from bookstack.models import Page, PageReview, Book

class PageReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=150)
    
    class Meta:
        model = PageReview
        fields = ('id', 'user', 'text', 'created_at')
        
        def get_user(self, obj):
            return obj.name


class PageSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    reviews = PageReviewSerializer(many=True)
    
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


class CreatePageReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PageReview
        fields = ('text',)
    
    def create(self, validated_data):
        page = get_object_or_404(Page, pk=self.context['page_slug'])
        validated_data['user'] = self.context['request'].user
        validated_data['page'] = page
        return super().create(validated_data)