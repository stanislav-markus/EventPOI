import json
import os
from datetime import datetime
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf import settings
#from django.core.cache import cache
from django.contrib.gis.geos import Polygon
from django.contrib.auth.models import User
from photologue.models import Gallery, Photo
from core.models import POI


class JSONSerialize(object):

    def __init__(self, resource):
        self.resource = resource

    def resource_to_json(self):
        r_list = self.resource.get_object_list(None)
        r_to_serialize = [self.resource.full_dehydrate(self.resource.build_bundle(obj=obj))
            for obj in r_list]
        return json.loads(self.resource.serialize(None, r_to_serialize, 'application/json'))

    def object_to_json(self, obj):
        bundle = self.resource.build_bundle(obj=obj)
        r_to_serialize = self.resource.full_dehydrate(bundle)
        return json.loads(self.resource.serialize(None, r_to_serialize, 'application/json'))


class JSONCache(object):
    
    def __init__(self):
        dirname = os.path.dirname(settings.TASTYPIE_JSON_CACHE)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if not os.path.exists(settings.TASTYPIE_JSON_CACHE):
            with open(settings.TASTYPIE_JSON_CACHE,"a+") as f:
                f.write('{}')

    def _load(self):
        data_file = open(settings.TASTYPIE_JSON_CACHE, 'r')
        return json.load(data_file)

    def _save(self, data):
        data_file = open(settings.TASTYPIE_JSON_CACHE, 'w')
        return json.dump(data, data_file)

    def get_all(self):
        #return cache.get_many([p.id for p in POI.objects.all()]).values()
        return sorted(self._load().values(), key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

    def delete(self, key):
        data = self._load()
        data.pop(str(key), None)
        self._save(data)

    def get(self, key):
        data = self._load()
        return data.get(key, None)

    def set(self, key, value):
        #cache.set(key, value, timeout=None)
        data = self._load()
        data[key] = value
        self._save(data)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username']
        filtering = {
            'username': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['avatar_url'] = bundle.obj.get_profile().photo.get_avatar_url()
        return bundle


class PhotoResource(ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        resource_name = 'photo'
        fields = ['image']

    def dehydrate(self, bundle):
        bundle.data['display_url'] = bundle.obj.get_display_url()
        bundle.data['thumbnail_url'] = bundle.obj.get_thumbnail_url()
        bundle.data['preview_url'] = bundle.obj.get_preview_url()
        bundle.data['view_count'] = bundle.obj.view_count
        return bundle


class GalleryResource(ModelResource):
    photos = fields.ToManyField(PhotoResource, 'photos', full=True, null=True, blank=True)

    class Meta:
        queryset = Gallery.objects.all()
        resource_name = 'gallery'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class POIResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    photo = fields.ForeignKey(PhotoResource, 'photo', full=True)

    class Meta:
        queryset = POI.objects.all()
        resource_name = 'poi'
        allowed_methods = ['get', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            "date": ['exact', 'range', 'lte', 'gte',],
        }
        ordering = ['date',]

    def dehydrate(self, bundle):
        del bundle.data['location']
        bundle.data['latitude'] = bundle.obj.location.x
        bundle.data['longitude'] = bundle.obj.location.y
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(POIResource, self).build_filters(filters)

        if('bbox' in filters):
            v_tmp = filters.get('bbox').split(',')
            orm_filters.update({
                'location__within': Polygon.from_bbox(v_tmp)
            })
        return orm_filters

    def get_object_list(self, request):
        return (
            super(POIResource, self)
            .get_object_list(request)
            .order_by('-date')
        )