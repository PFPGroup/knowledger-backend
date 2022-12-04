from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookstack.serializers.book_serializers import (
    BooksSerializer, BookDetailSerializer, CreateUpdateBookSerializer,
    BookActivitySerializer,
)
from bookstack.models import (
    Book, Activity
)


class BookViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    extra_kwargs = {
            'url': {'lookup_field': 'slug'}
            }
    
    def retrieve(self, request, *args, **kwargs):
        self.queryset = Book.objects.filter(shelve__slug=self.kwargs['shelve_slug']).prefetch_related('chapter')
        instance = self.get_object()
        serializer = BookDetailSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.creature.id == request.user.id:
            return Response(
                {'error': 'no permission'},
                status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Book.objects.filter(shelve__slug=self.kwargs['shelve_slug'])

    def get_serializer_class(self):
        if not self.request.method == 'GET':
            return CreateUpdateBookSerializer
        return BooksSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user': self.request.user
        }


class BookActivityView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(model_type='book', book__slug=self.kwargs['pk'])