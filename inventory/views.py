from django.shortcuts import render
from rest_framework import generics
from inventory.models import MuseumObject
from inventory.serializers import MuseumObjectSerializer


class MuseumObjectList(generics.ListAPIView):
    queryset = MuseumObject.objects.all()
    serializer_class = MuseumObjectSerializer


class MuseumObjectDetail(generics.RetrieveAPIView):
    queryset = MuseumObject.objects.all()
    serializer_class = MuseumObjectSerializer
