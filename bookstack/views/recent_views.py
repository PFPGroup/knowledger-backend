from rest_framework.generics import (
    ListAPIView
)
from bookstack.models import (
    Book, Page, Activity
)
from bookstack.serializers.main_serializers import (
    ActivitySerializer, RecentBookSerializer, RecentPageSerializer
)

# Create your views here.

class ActivityView(ListAPIView):
    queryset = Activity.objects.all()[:10]
    serializer_class = ActivitySerializer


class RecentBookView(ListAPIView):
    queryset = Book.objects.filter(published=True).values('name', 'slug').order_by('created_at')[:10]
    serializer_class = RecentBookSerializer


class RecentPageView(ListAPIView):
    queryset = Page.objects.filter(chapter__book__published=True).values('text', 'slug').order_by('updated_at')[:10]
    serializer_class = RecentPageSerializer