#!/usr/bin/env python3
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import EmailField
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


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
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["password"]
