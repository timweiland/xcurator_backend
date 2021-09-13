#!/usr/bin/env python3
from rest_framework import serializers
from inventory.models import (
    MuseumObject,
    Collection,
    Museum,
    CollectionDomain,
    ObjectSubject,
    ObjectCreator,
    ObjectPublisher,
    LanguageCode,
    ObjectImage,
    ImageColor,
    ObjectLocation,
    ObjectLocationType,
    ObjectDateType,
    ObjectDate,
    ObjectTitle,
)


class MuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museum
        fields = ["name"]


class CollectionDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionDomain
        fields = ["name"]


class CollectionSerializer(serializers.ModelSerializer):
    museum = MuseumSerializer(read_only=True)
    domain = CollectionDomainSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ["museum", "name", "domain"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectSubject
        fields = ["name"]


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectCreator
        fields = ["name"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPublisher
        fields = ["name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageCode
        fields = ["code"]


class ImageColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageColor
        fields = ["value"]


class ObjectImageSerializer(serializers.ModelSerializer):
    color = ImageColorSerializer(many=True, read_only=True)

    class Meta:
        model = ObjectImage
        fields = ["image", "color"]


class ObjectLocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectLocationType
        fields = ["name"]


class ObjectLocationSerializer(serializers.ModelSerializer):
    location_type = ObjectLocationTypeSerializer(read_only=True)

    class Meta:
        model = ObjectLocation
        fields = ["location_type", "term", "location"]


class ObjectDateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectDateType
        fields = ["name"]


class ObjectDateSerializer(serializers.ModelSerializer):
    type = ObjectDateTypeSerializer(read_only=True)

    class Meta:
        model = ObjectDate
        fields = ["type", "value"]


class ObjectTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectTitle
        fields = ["title"]


class MuseumObjectSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(many=True, read_only=True)
    subject = SubjectSerializer(many=True, read_only=True)
    creator = CreatorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)
    objectimage_set = ObjectImageSerializer(many=True, read_only=True)
    objectlocation_set = ObjectLocationSerializer(many=True, read_only=True)
    objectdate_set = ObjectDateSerializer(many=True, read_only=True)
    objecttitle_set = ObjectTitleSerializer(many=True, read_only=True)

    class Meta:
        model = MuseumObject
        fields = [
            "collection",
            "internal_identifier",
            "subject",
            "description",
            "creator",
            "publisher",
            "language",
            "objectimage_set",
            "objectlocation_set",
            "objectdate_set",
            "objecttitle_set",
        ]
