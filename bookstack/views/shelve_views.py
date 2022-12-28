from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from bookstack.models import (
    Shelve, Activity
)
from bookstack.serializers.shelve_serializers import (
    ShelveSerializer, NewShelveSerializer, CreateUpdateShelveSerializer,
    ShelveDetailSerializer, ShelveActivitySerializer,
)
from bookstack.filters import  ShelveFilterset

# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class ShelveViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ShelveFilterset
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    queryset = Shelve.objects.all().prefetch_related('books')
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'},
    }
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shelve = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=1,
            model_type='shelve',
            shelve=shelve,
            name=shelve.name,
            slug=shelve.slug
        )
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        shelve = serializer.save()
        Activity.objects.create(
            user=request.user,
            activity=2,
            model_type='shelve',
            shelve=shelve,
            name=shelve.name,
            slug=shelve.slug
        )
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.id == instance.creature.id:
            return Response(
                {'permission': 'permission denied'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        self.perform_destroy(instance)
        Activity.objects.create(
            user=request.user,
            activity=3,
            model_type='shelve',
            name=instance.name
        )
        return Response({'ok': 'object has been deleted successfully'})
    
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return CreateUpdateShelveSerializer
        elif self.action == 'retrieve':
            return ShelveDetailSerializer
        else:
            return ShelveSerializer


class NewShelveView(ListAPIView):
    queryset = Shelve.objects.filter(is_active=True).values('name','slug').order_by('-updated_at')
    serializer_class = NewShelveSerializer


class ShelveActivityView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ShelveActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(model_type='shelve', is_active=True)