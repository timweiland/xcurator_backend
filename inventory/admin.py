from django.contrib import admin
import django.contrib.gis.admin as geo_admin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget
from .models import (
    ObjectLocation,
    MuseumObject,
    Collection,
    CollectionDomain,
    Museum,
    ObjectTitle,
    ObjectLocation,
    ObjectDate,
    ObjectImage,
)


class GoogleMapsWidgetAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}


geo_admin.site.register(ObjectLocation, GoogleMapsWidgetAdmin)


class TitleInline(admin.TabularInline):
    model = ObjectTitle
    extra = 0


class LocationInline(admin.TabularInline):
    model = ObjectLocation
    extra = 0


class DateInline(admin.TabularInline):
    model = ObjectDate
    extra = 0


class ImageInline(admin.TabularInline):
    model = ObjectImage
    extra = 0


class MuseumObjectAdmin(admin.ModelAdmin):
    inlines = [TitleInline, LocationInline, DateInline, ImageInline]


admin.site.register(Museum)
admin.site.register(CollectionDomain)
admin.site.register(Collection)
admin.site.register(MuseumObject, MuseumObjectAdmin)
