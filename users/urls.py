#!/usr/bin/env python3
from django.urls import path, include
from users import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("refresh/", views.RefreshTokenView.as_view()),
    path("profile/", views.ProfileView.as_view()),
]
