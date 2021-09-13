from django.db import models
import django.contrib.gis.db.models as geo_models


class ObjectLocationType(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class ObjectSubject(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class ObjectCreator(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class ObjectDateType(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class ObjectPublisher(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class LanguageCode(models.Model):
    code = models.CharField(max_length=6, default="")

    def __str__(self):
        return self.code


class Museum(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class CollectionDomain(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Collection(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="")
    domain = models.ForeignKey(CollectionDomain, blank=True, on_delete=models.CASCADE)


class MuseumObject(models.Model):
    collection = models.ManyToManyField(Collection)
    internal_identifier = models.CharField(max_length=100, default="")
    subject = models.ManyToManyField(ObjectSubject, blank=True)
    description = models.CharField(max_length=5000, default="", blank=True)
    creator = models.ManyToManyField(ObjectCreator, blank=True)
    publisher = models.ManyToManyField(ObjectPublisher)
    language = models.ManyToManyField(LanguageCode)

    def __str__(self):
        for title in self.objecttitle_set.all():
            return f"{title} ({self.pk})"
        return f"{self.internal_identifier}"


class ImageColor(models.Model):
    value = models.CharField(max_length=80)

    def __str__(self):
        return self.value


class ObjectImage(models.Model):
    museum_object = models.ForeignKey(MuseumObject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    color = models.ManyToManyField(ImageColor)


class ObjectLocation(models.Model):
    location_type = models.ForeignKey(ObjectLocationType, on_delete=models.CASCADE)
    term = models.CharField(max_length=200, default="")
    location = geo_models.PointField()
    museum_object = models.ForeignKey(MuseumObject, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.location_type}] {self.term} {self.location}"


class ObjectDate(models.Model):
    type = models.ForeignKey(ObjectDateType, on_delete=models.CASCADE)
    value = models.CharField(max_length=80, default="")
    museum_object = models.ForeignKey(MuseumObject, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.type}] {self.value} - {self.museum_object}"


class ObjectTitle(models.Model):
    title = models.CharField(max_length=1000, default="")
    museum_object = models.ForeignKey(MuseumObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
