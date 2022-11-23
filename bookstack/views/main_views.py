from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveAPIView, ListAPIView
)
from rest_framework.views import APIView

from bookstack.models import (
    Book, Page, Activity
)
from bookstack.serializers import (
    ActivitySerializer, RecentBookSerializer, RecentPageSerializer
)

# Create your views here.

class ActivityView(ListAPIView):
    queryset = Activity.objects.all()[:10]
    serializer_class = ActivitySerializer


class BookView(ListAPIView):
    queryset = Book.objects.all().values('name', 'slug').order_by('created_at')[:10]
    serializer_class = RecentBookSerializer


class PageView(ListAPIView):
    queryset = Page.objects.all().values('text', 'slug').order_by('updated_at')[:10]
    serializer_class = RecentPageSerializer