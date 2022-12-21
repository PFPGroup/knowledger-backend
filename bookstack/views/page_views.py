from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from bookstack.serializers.page_serializers import (
    PageSerializer, UpdateCreatePageSerializer, CreatePageReviewSerializer
)
from bookstack.models import (
    Page, Book, PageImage, PageReview, Activity
)
from bookstack.filters import PageFilterset


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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PageFilterset
    search_fields = ['name', 'text']
    ordering_fields = ['name', 'created_at', 'updated_at']
    lookup_field = 'slug'
    extra_kwargs = {
            'url': {'lookup_field': 'slug'}
            }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=1,
            model_type='page',
            page=page,
            name=page.name,
            slug=page.slug
        )
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        page = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=2,
            model_type='page',
            page=page,
            name=page.name,
            slug=page.slug
        )
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        if request.user in book.authors.all():
            instance = self.get_object()
            self.perform_destroy(instance)
            Activity.objects.create(
            user=request.user,
            activity=3,
            model_type='page',
            name=instance.name,
            )

            return Response({'ok': 'object has been deleted successfully'})
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
            'book_slug': self.kwargs['book_slug'],
            'chapter_pk': self.kwargs['chapter_pk'],
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