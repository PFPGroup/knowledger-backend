from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView,
)
from django.contrib.auth import get_user_model

from .serializers import (
    CostumeTokenObtainPairSerializer, RegisterSerializer,ChangePasswordSerializer
)
# Create your views here.

User = get_user_model()

class CostumeTokenObtainPairView(TokenObtainPairView):
    serializer_class = CostumeTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer