from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CostumeTokenObtainPairView, RegisterView, ChangePasswordView, UpdateUserView, LogoutView
)


urlpatterns = [
    path('api/token/', CostumeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/registeration/', RegisterView.as_view(), name='auth_register'),
    path('api/updateuser/<int:pk>', UpdateUserView.as_view(), name='auth_update_profile'),
    path('api/password/change/<int:pk>', ChangePasswordView.as_view(), name='auth_change_password'),
]
