from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from bookstack.models import Chapter, Book
from bookstack.serializers.chapter_serializers import (
    ChapterSerializer, ChapterDetailSerializer, CreateUpdateChapterSerializer
)
from bookstack.filters import ChapterFilterset


class ChapterViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ChapterFilterset
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        authors = get_object_or_404(Book, slug=self.kwargs['book_slug']).authors.all()
        if request.user in authors:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request, *args, **kwargs):
        authors = get_object_or_404(Book, slug=self.kwargs['book_slug']).authors.all()
        if request.user in authors:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        if not book.creature.id == request.user.id:
            return Response(
                {'error': 'no permission'},
                status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Chapter.objects.filter(book__slug=self.kwargs['book_slug'], book__published=True)
    
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
