from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from bookstack.serializers.page_serializers import (
    PageSerializer, UpdateCreatePageSerializer, CreatePageReviewSerializer
)
from bookstack.models import Page, Book, PageReview

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'


class PageViewset(ListModelMixin,
                CreateModelMixin,
                UpdateModelMixin,
                DestroyModelMixin,
                GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    
    
    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        if request.user in book.authors.all():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {'permission': 'you have no permissions to delete this book'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def get_serializer_class(self):
        action_lst = ('update', 'partial_update', 'create',)
        if self.action in action_lst:
            return UpdateCreatePageSerializer
        else:
            return PageSerializer
    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'book_slug': self.kwargs['book_slug']
        }
    
    def get_queryset(self):
        return Page.objects.filter(chapter__id=self.kwargs['chapter_pk']).prefetch_related('reviews')


class PageReviewViewset(CreateModelMixin,
                        DestroyModelMixin,
                        GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatePageReviewSerializer
    queryset = PageReview.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        review = get_object_or_404(PageReview, pk=self.kwargs['pk'])
        if request.user.is_staff or (request.user == review.user):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {'permission': 'you have no permissions to delete this book'},
                status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'page_slug': self.kwargs['page_pk']
        }