from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
)

from bookstack.models import (
    Shelve,
)
from bookstack.serializers import (
ShelveSerializer, NewShelveSerializer, CreateShelveSerializer
)

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class ShelveView(ListAPIView):
    queryset = Shelve.objects.all().prefetch_related('books')
    serializer_class = ShelveSerializer


class NewShelveView(ListAPIView):
    queryset = Shelve.objects.all().values('name').order_by('created_at')
    serializer_class = NewShelveSerializer


class CreateShelveView(CreateAPIView):
    model = Shelve
    serializer_class = CreateShelveSerializer
    permission_classes = (IsAuthenticated,)