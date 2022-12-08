from django.urls import path, include
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
from bookstack.views.chapter_views import ChapterViewSet
from bookstack.views.page_views import PageViewset

router = routers.DefaultRouter()
router.register(r'shelves', ShelveViewset, basename='shelves')

books_router = routers.NestedDefaultRouter(router, 'shelves', lookup='shelve')
books_router.register(r'books', BookViewset, basename='books')

chapter_router = routers.NestedDefaultRouter(books_router, 'books', lookup='book' )
chapter_router.register(r'chapter', ChapterViewSet, basename='chapter')

page_router = routers.NestedDefaultRouter(chapter_router, 'chapter', lookup='chapter')
page_router.register(r'page', PageViewset, basename='page')


urlpatterns = [
    # nested routers
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('', include(chapter_router.urls)),
    path('', include(page_router.urls)),
    # recent views
    path('recent/books/', RecentBookView.as_view(), name='recent_bookview'),
    path('recent/pages/', RecentPageView.as_view(), name='recent_pageview'),
    path('recent/shelves/', NewShelveView.as_view(), name='recent_helves'),
    # activity views
    path('activities/', ActivityView.as_view(), name='recent_activity'),
    path('activities/shelves/', ShelveActivityView.as_view(), name='recent_shelveactivity'),
    path('activities/book/<slug:pk>/', BookActivityView.as_view(), name='book_activity'),
]
