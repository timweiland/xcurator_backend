from pathlib import Path
import zipfile
import json
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from inventory.models import (
    MuseumObject,
    Museum,
    Collection,
    CollectionDomain,
    ObjectSubject,
    ObjectCreator,
    ObjectPublisher,
    LanguageCode,
    ObjectTitle,
    ObjectDateType,
    ObjectDate,
    ObjectLocationType,
    ObjectLocation,
    ObjectImage,
    ImageColor,
)


def create_collections(collection_data, museum_object):
    for collection_record in collection_data:
        museum, _ = Museum.objects.get_or_create(name=collection_record["museum"])
        domain, _ = CollectionDomain.objects.get_or_create(
            name=collection_record["domain"]
        )
        collection, _ = Collection.objects.get_or_create(
            museum=museum, name=collection_record["name"], domain=domain
        )
        collection.save()
        museum_object.collection.add(collection)


def create_subjects(subject_data, museum_object):
    for subject_record in subject_data:
        subject, _ = ObjectSubject.objects.get_or_create(name=subject_record)
        museum_object.subject.add(subject)


def create_creators(creator_data, museum_object):
    for creator_record in creator_data:
        creator, _ = ObjectCreator.objects.get_or_create(name=creator_record)
        museum_object.creator.add(creator)


def create_publishers(publisher_data, museum_object):
    for publisher_record in publisher_data:
        publisher, _ = ObjectPublisher.objects.get_or_create(name=publisher_record)
        museum_object.publisher.add(publisher)


def create_languages(language_data, museum_object):
    for language_record in language_data:
        language, _ = LanguageCode.objects.get_or_create(code=language_record)
        museum_object.language.add(language)


def create_titles(title_data, museum_object):
    for title_record in title_data:
        title, _ = ObjectTitle.objects.get_or_create(
            title=title_record, museum_object=museum_object
        )


def create_dates(date_data, museum_object):
    for date_record in date_data:
        date_type, _ = ObjectDateType.objects.get_or_create(name=date_record["type"])
        date, _ = ObjectDate.objects.get_or_create(
            type=date_type, value=date_record["value"], museum_object=museum_object
        )


def create_locations(location_data, museum_object):
    for location_record in location_data:
        location_type, _ = ObjectLocationType.objects.get_or_create(
            name=location_record["type"]
        )
        lon = (
            float(location_record["lon"])
            if location_record["lon"] is not None
            else None
        )
        lat = (
            float(location_record["lat"])
            if location_record["lat"] is not None
            else None
        )
        point = Point(0, 0)
        if lon is not None and lat is not None:
            point = Point(lon, lat)
        object_location, _ = ObjectLocation.objects.get_or_create(
            location_type=location_type,
            term=location_record["term"],
            location=point,
            museum_object=museum_object,
        )


def create_image_colors(color_data, object_image):
    for color in color_data:
        image_color, _ = ImageColor.objects.get_or_create(value=color)
        object_image.color.add(image_color)


def create_images(image_data, archive, museum_object):
    for image_record in image_data:
        object_image = ObjectImage(museum_object=museum_object)
        img_path = image_record["path"]
        try:
            content_file = ContentFile(archive.read(img_path))
        except KeyError:
            return
        object_image.image.save(img_path, ContentFile(archive.read(img_path)), True)
        if "colors" in image_record:
            create_image_colors(image_record["colors"], object_image)
        object_image.save()


def handle_record(record, archive):
    print(record)
    museum_object, _ = MuseumObject.objects.get_or_create(
        internal_identifier=record["identifier"]
    )
    print(museum_object)
    museum_object.description = record["description"]

    create_collections(record["collection"], museum_object)
    create_subjects(record["subject"], museum_object)
    create_creators(record["creator"], museum_object)
    create_publishers(record["publisher"], museum_object)
    create_languages(record["language"], museum_object)
    create_titles(record["title"], museum_object)
    create_dates(record["date"], museum_object)
    create_locations(record["coverage"], museum_object)
    create_images(record["media"], archive, museum_object)

    museum_object.save()
    print(museum_object)


class Command(BaseCommand):
    help = "Import museum objects in DC format from a zip file"

    def add_arguments(self, parser):
        parser.add_argument("--zip-path", type=str)

    def handle(self, *args, **options):
        zip_path = Path(options["zip_path"])
        if not zip_path.is_file():
            raise CommandError("Invalid zip path")
        archive = zipfile.ZipFile(str(zip_path), "r")
        json_data = archive.read("dc.json")
        data = json.loads(json_data)
        for record in data:
            handle_record(record, archive)
