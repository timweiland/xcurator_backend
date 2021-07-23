from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from users.serializers import RegisterSerializer

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
