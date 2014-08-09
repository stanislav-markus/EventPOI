from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views

from tastypie.api import Api
from registration.backends.default.views import RegistrationView
from core.forms import RegistrationFormWithName
from core.api import UserResource, PhotoResource, GalleryResource, POIResource 
from core.views import (POIListVIew, GalleryView,
    POICreateView, POIDetailView, POIDeleteView, POIUpdateView,
    UserProfileCreateView, UserProfileDetailView, UserProfileUpdateView)

poi_resource = POIResource()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PhotoResource())
v1_api.register(GalleryResource())
v1_api.register(POIResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^gallery/filter/(?P<cond>[\-\d\w]+)/page/(?P<page>[0-9]+)/$', GalleryView.as_view(), name='gallery'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
	url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
	url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
	url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
	url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
	url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormWithName), 
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/add/$', UserProfileCreateView.as_view(), name='profile_add'),
    url(r'^profile/(?P<slug>[\-\d\w]+)/$', UserProfileDetailView.as_view(), name='profile_detail'),
    url(r'^profile/(?P<slug>[\-\d\w]+)/update/$', UserProfileUpdateView.as_view(), name='profile_update'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^photologue/', include('photologue.urls')),
    url(r'^pois/', POIListVIew),
    url(r'^(?P<slug>[\-\d\w]+)/$', POIDetailView.as_view(), name='poi_detail'),
    url(r'^poi/add/$', POICreateView.as_view(), name='poi_add'),
    url(r'^(?P<slug>[\-\d\w]+)/update/$', POIUpdateView.as_view(), name='poi_update'),
    url(r'^poi/(?P<slug>[\-\d\w]+)/delete/$', POIDeleteView.as_view(), name='poi_delete'),
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
