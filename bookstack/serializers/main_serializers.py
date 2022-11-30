from rest_framework import serializers

from bookstack.models import (
    Activity, Book, Page
)



class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('user', 'activity', 'created_at', 'name', 'slug')


class RecentBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('name', 'slug')


class RecentPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('text', 'slug')