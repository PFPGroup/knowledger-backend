from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CostumeTokenObtainPairView, RegisterView, ChangePasswordView, UpdateUserView, LogoutView, ActivateAccount
)


urlpatterns = [
    path('login/', CostumeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('registeration/', RegisterView.as_view(), name='auth_register'),
    path('updateuser/<int:pk>', UpdateUserView.as_view(), name='auth_update_profile'),
    path('password/change/<int:pk>', ChangePasswordView.as_view(), name='auth_change_password'),
    path('activate-email/<str:uidb64>/<str:token>/', ActivateAccount.as_view(), name='account_activate'),
]
