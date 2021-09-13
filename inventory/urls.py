#!/usr/bin/env python3
from django.urls import path, include
from inventory import views

urlpatterns = [
    path("museum-objects/", views.MuseumObjectList.as_view()),
    path("museum-objects/<int:pk>", views.MuseumObjectDetail.as_view()),
]
