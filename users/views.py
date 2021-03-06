import datetime as dt
import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken as RefreshTokenModel

from users.serializers import RegisterSerializer, UserSerializer
import users.token_serializers as token_serializers
from users.tokens import account_activation_token

UserModel = get_user_model()


class TokenViewBaseWithCookie(TokenViewBase):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        resp = Response(serializer.validated_data, status=status.HTTP_200_OK)

        expiration = dt.datetime.fromtimestamp(
            serializer.validated_data["refresh_expires"]
        )

        resp.set_cookie(
            settings.JWT_COOKIE_NAME,
            serializer.validated_data["refresh"],
            expires=expiration,
            secure=settings.JWT_COOKIE_SECURE,
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE,
        )

        return resp


class LoginView(TokenViewBaseWithCookie):
    serializer_class = token_serializers.TokenObtainPairSerializer


class RefreshTokenView(TokenViewBaseWithCookie):
    serializer_class = token_serializers.TokenRefreshSerializer


class LogoutView(APIView):
    def post(self, *args, **kwargs):
        resp = Response({})
        token = self.request.COOKIES.get(settings.JWT_COOKIE_NAME)
        refresh = RefreshTokenModel(token)
        try:
            refresh.blacklist()
        except AttributeError:
            # Blacklist not available
            pass
        resp.delete_cookie(settings.JWT_COOKIE_NAME)
        return resp


class RegisterView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class ActivateAccountView(APIView):
    def patch(self, request, uidb64, token, format=None):
        try:
            uid = base64.urlsafe_b64decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
