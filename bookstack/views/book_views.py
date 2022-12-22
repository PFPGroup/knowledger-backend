from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from bookstack.serializers.book_serializers import (
    BooksSerializer, BookDetailSerializer, CreateUpdateBookSerializer,
    BookActivitySerializer,
)
from bookstack.models import (
    Book, BookViews, Activity,
)
from bookstack.filters import BookFilterset

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class BookViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilterset
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    extra_kwargs = {
            'url': {'lookup_field': 'slug'}
            }
    
    def check_client_ip(self, instance, ip):
        ip_obj, created = BookViews.objects.get_or_create(
            book=instance,
            ip_address=ip,
        )
        return created
    
    def retrieve(self, request, *args, **kwargs):
        self.queryset = Book.objects.filter(shelve__slug=self.kwargs['shelve_slug']).prefetch_related('chapter')
        instance = self.get_object()
        created = self.check_client_ip(instance, request.META.get('REMOTE_ADDR'))
        if created:
            instance.views_count += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=1,
            model_type='book',
            book=book,
            name=book.name,
            slug=book.slug
        )
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=2,
            model_type='book',
            book=book,
            name=book.name,
            slug=book.slug
        )
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.creature.id == request.user.id:
            return Response(
                {'error': 'no permission'},
                status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        Activity.objects.create(
            user=request.user,
            activity=3,
            model_type='shelve',
            name=instance.name
        )
        return Response({'ok': 'object has been deleted successfully'})
    
    def get_queryset(self):
        return Book.objects.filter(shelve__slug=self.kwargs['shelve_slug'])

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateUpdateBookSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        else:
            return BooksSerializer
    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'shelve_slug': self.kwargs['shelve_slug']
        }


class BookActivityView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(model_type='book', book__slug=self.kwargs['pk'])