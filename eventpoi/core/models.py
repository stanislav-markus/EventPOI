import os, random
from shutil import copyfile
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from photologue.models import Photo
from core.utils import unique_slugify


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

MEDIA_DIR = settings.MEDIA_ROOT if settings.OPENSHIFT else 'public/media'


class POI(models.Model):
    location = models.PointField(srid=4326)
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70)
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    like_count = models.PositiveIntegerField(default=0)

    objects = models.GeoManager()

    def get_absolute_url(self):
        return reverse('poi_detail', args=[self.slug])

    def as_json(self):
        from core.api import JSONSerialize, POIResource
        return JSONSerialize(POIResource()).object_to_json(self)

    def delete(self, *args, **kwargs):
        from core.api import JSONCache
        JSONCache().delete(self.id)
        super(POI, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        from core.api import JSONCache
        unique_slugify(self, self.name)
        super(POI, self).save(*args, **kwargs)

        JSONCache().set(self.id, self.as_json())

    def __unicode__(self):
        return u'{}'.format(self.name)


class UserProfile(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user = models.ForeignKey(User, unique=True)
    photo = models.ForeignKey(Photo, null=True)
    location = models.PointField(srid=4326, null=True)
    slug = models.SlugField(max_length=70)

    def get_points(self):
        return POI.objects.filter(user=self.user).order_by('-date')

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        unique_slugify(self, self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.user.username)


def get_default_avatar(gender):
    avatar_dir = os.path.join(settings.STATIC_ROOT,
        'images', '60-male-female-avatars', dict(GENDER_CHOICES)[gender])
    avatar_filename = random.choice(os.listdir(avatar_dir))
    avatar_src_file = os.path.join(avatar_dir, avatar_filename)
    avatar_dst_file = os.path.join(MEDIA_DIR, avatar_filename)
    dirname = os.path.dirname(avatar_dst_file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    copyfile(avatar_src_file, avatar_dst_file)
    photo = Photo(image=File(open(avatar_dst_file)))
    unique_slugify(photo, avatar_filename)
    photo.title = photo.slug
    photo.save()
    return photo

 
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.gender = request.POST["gender"]
    profile.photo = get_default_avatar(profile.gender)
    profile.save()
 
user_registered.connect(user_registered_callback)
