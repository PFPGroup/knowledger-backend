from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from .views.recent_views import (
    ActivityView, RecentPageView, RecentBookView,
)
from bookstack.views.shelve_views import (
    ShelveViewset, NewShelveView, ShelveActivityView
)
from bookstack.views.book_views import (
    BookActivityView, BookViewset
)
from bookstack.views.chapter_views import(
    ChapterViewSet
)

router = routers.DefaultRouter()
router.register(r'books', BookViewset, basename='books')
router.register(r'shelves', ShelveViewset, basename='shelves')

chapter_router = routers.NestedDefaultRouter(router, 'books', lookup='book' )
chapter_router.register('chapter', ChapterViewSet, basename='chapter')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(chapter_router.urls)),
    # recent views
    path('recent/activities/', ActivityView.as_view(), name='recent_activity'),
    path('recent/books/', RecentBookView.as_view(), name='recent_bookview'),
    path('recent/pages/', RecentPageView.as_view(), name='recent_pageview'),
    path('recent/shelves/', NewShelveView.as_view(), name='recent_helves'),
    path('recent/shelves-activity/', ShelveActivityView.as_view(), name='recent_shelveactivity'),
    # book views
    path('books/<slug:pk>/activity/', BookActivityView.as_view(), name='book_activity'),
]
