from django.urls import path

from .views.main_views import (
    ActivityView, BookView, PageView,
)
from .views.shelve_views import (
    ShelveView, NewShelveView, CreateShelveView
)

urlpatterns = [
    path('activityview/', ActivityView.as_view(), name='activityview'),
    path('bookview/', BookView.as_view(), name='bookview'),
    path('pageview/', PageView.as_view(), name='pageview'),
    path('shelves/', ShelveView.as_view(), name='shelveview'),
    path('newshelves/', NewShelveView.as_view(), name='newshelvesview'),
    path('create_shelve/', CreateShelveView.as_view(), name='create_shelve')
]
