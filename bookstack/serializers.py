from rest_framework import serializers

from .models import (
    Activity, Book, Page, Shelve,
    )

from taggit.serializers import (
    TagListSerializerField, TaggitSerializer
    )

class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = ('user', 'activity', 'book', 'page', 'created_at',)


class RecentBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ('name', 'slug')

class RecentPageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page
        fields = ('text', 'slug')


class ShelveSerializer(serializers.ModelSerializer):
    books = RecentBookSerializer(many=True)
    
    class Meta:
        model = Shelve
        fields = ('name', 'description', 'slug', 'created_at', 'updated_at', 'image', 'books' )


class NewShelveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shelve
        fields = ('name',)


# class CreateShelveSerializer(TaggitSerializer, serializers.ModelSerializer):
#     tags = TagListSerializerField()
    
#     class Meta:
#         model = Shelve
#         fields = ('name', 'description', 'image', 'tags')
    
#     def create(self, validated_data):
#         Shelve.objects.create(
#             user = self.request.user
#             name = validated_data['name']
#             description = validated_data['description']
#             image = 
#         )