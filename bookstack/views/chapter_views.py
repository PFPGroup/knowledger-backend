from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from bookstack.models import Chapter, Book
from bookstack.serializers.chapter_serializers import (
    ChapterSerializer, ChapterDetailSerializer, CreateUpdateChapterSerializer
)

class ChapterViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def retrieve(self, request, *args, **kwargs):
        self.queryset = Chapter.objects.filter(book__slug=self.kwargs['book_slug']).prefetch_related('page')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        if not book.creature.id == request.user.id:
            return Response(
                {'error': 'no permission'},
                status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Chapter.objects.filter(book__slug=self.kwargs['book_slug'])
    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'book_slug': self.kwargs['book_slug'],
        }
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChapterDetailSerializer
        elif self.action == 'update' or self.action == 'create':
            return CreateUpdateChapterSerializer
        return ChapterSerializer
