from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail 

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404

from .serializers import (
    CostumeTokenObtainPairSerializer, RegisterSerializer,
    ChangePasswordSerializer, UpdateUserSerializer, LogoutSerializer
)
from rest_framework import status
from core.tokens import account_activation_token

# Create your views here.

User = get_user_model()

class CostumeTokenObtainPairView(TokenObtainPairView):
    serializer_class = CostumeTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        current_site = get_current_site(self.request)
        uid64 = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)
        subject = 'Activate Your BookStack Account'
        message = f"""Please click on the following link to activate your account
        {current_site.domain}/auth/activate-email/{uid64}/{token}"""
        try:
            send_mail(
                subject=subject,
                from_email=None,
                message=message,
                recipient_list=[f'{user.email}'],
                fail_silently=False
            )
            return Response({'message': 'Please Confirm your email to complete registration.'})
        except:
            user.delete()
            return Response({'error': 'please try again somthing went wrong!'})


class ActivateAccount(APIView):
    http_method_names = ['get']

    def get(self, request, uidb64, token):
        uid =force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=uid)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'success': 'Account activated'})
        else:
            return Response({'failure': 'token is invalid'})


class ChangePasswordView(UpdateAPIView):
    http_method_names = ['put']
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateUserView(RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch']
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
