#!/usr/bin/env python3
import base64
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.fields import EmailField
from rest_framework.validators import UniqueValidator
from users.tokens import account_activation_token

UserModel = get_user_model()


def send_activation_mail(user):
    subject = "Activate your xCurator account"
    message = render_to_string(
        "account_activation_email.html",
        {
            "user": user,
            "frontend_base": settings.FRONTEND_BASE,
            "uid": base64.urlsafe_b64encode(str(user.pk).encode()).decode(),
            "token": account_activation_token.make_token(user),
        },
    )
    recipient = user.email
    email = EmailMessage(subject, message, to=[recipient])
    email.send()


class RegisterSerializer(serializers.ModelSerializer):
    email = EmailField(
        allow_blank=False,
        label="Email address",
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(
                queryset=UserModel.objects.all(),
                message="This email address is already in use.",
            )
        ],
    )

    class Meta:
        model = UserModel
        fields = ["email", "username", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.is_active = False
        user.email_confirmed = False
        user.save()
        send_activation_mail(user)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["password"]
