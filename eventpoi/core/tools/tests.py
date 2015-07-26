import json
import os
import urllib
import traceback

from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.template.defaultfilters import slugify
from core.utils import unique_slugify

from photologue.models import Photo
from core.models import POI

from reverse_geocode import get_address
import wikipedia

TEST_FILENAME = 'core/tools/test_data.json'

MEDIA_DIR = '../static/media' if settings.OPENSHIFT else 'public/media'

class URLopener(urllib.FancyURLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise Exception


def get_description(lat, lon, title):
    address = ''
    try:
        address = u'Address: {}'.format(get_address(lat, lon))
    except:
        pass
    found = wikipedia.search(title)
    if found:
        try:
            found = u"{} \n {}".format(wikipedia.summary(found[0])[:400], address)
        except:
            pass
    return found or address


def upload_data():

    with open(TEST_FILENAME) as f:
        data = json.loads(f.read())

    user = User.objects.all()[0]

    skipped = 0

    for i, point in enumerate(data):
        try:
            photo_file_url = point['photo_file_url']
            photo_title = point['photo_title'][:30]
            photo_location = Point(point['latitude'], point['longitude'])

            photo_filename = '{}.jpg'.format(slugify(photo_title))
            photo_file = URLopener().retrieve(photo_file_url,
                os.path.join(MEDIA_DIR, photo_filename))

            photo = Photo(image=File(open(photo_file[0])))
            unique_slugify(photo, photo_title)
            photo.title = photo.slug
            photo.save()

            poi = POI()
            poi.location = photo_location
            poi.name = photo_title
            poi.description = get_description(
                point['latitude'], point['longitude'], photo_title)
            poi.user = user
            poi.photo = photo
            poi.save()

            print i, photo_title, 'Saved.'
        except Exception:
            print traceback.format_exc()
            skipped += 1

    print skipped, 'POIs were skipped.'
