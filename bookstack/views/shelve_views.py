from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from bookstack.models import (
    Shelve, Activity
)
from bookstack.serializers.shelve_serializers import (
    ShelveSerializer, NewShelveSerializer, CreateUpdateShelveSerializer,
    ShelveDetailSerializer, ShelveActivitySerializer,
)

# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class ShelveViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Shelve.objects.all().prefetch_related('books')
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'},
    }
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.id == instance.creature.id:
            return Response(
                {'permission': 'permission denied'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.id == instance.creature.id:
            return Response(
                {'permission': 'permission denied'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return CreateUpdateShelveSerializer
        elif self.action == 'retrieve':
            return ShelveDetailSerializer
        else:
            return ShelveSerializer


class NewShelveView(ListAPIView):
    queryset = Shelve.objects.all().values('name','slug').order_by('-created_at')
    serializer_class = NewShelveSerializer


class ShelveActivityView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ShelveActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(model_type=1)