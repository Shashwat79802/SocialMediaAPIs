from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginInSerializer, SignUpSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class LoginInView(TokenObtainPairView):
    serializer_class = LoginInSerializer
    permission_classes = [AllowAny]
