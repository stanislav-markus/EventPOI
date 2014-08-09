import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.gis.geos import Point
from core.models import POI, UserProfile
from core.forms import POIForm, PhotoForm, PhotoUpdateForm, UserProfileForm
from core.api import JSONCache


def POIListVIew(request):
    data = {'objects': JSONCache().get_all()}
    return HttpResponse(json.dumps(data), content_type='application/json')


class GalleryView(ListView):
    queryset = POI.objects.all()
    paginate_by = 150
    template_name = 'gallery.html'

    def get_queryset(self):
        qs = super(GalleryView, self).get_queryset()
        qs_filtered = qs.order_by('-{}'.format(self.kwargs['cond']))
        return qs_filtered

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['cond'] = self.kwargs['cond']
        return context


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class POICreateView(CreateView):
    model = POI
    form_class = POIForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(POICreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(POICreateView, self).get_context_data(**kwargs)
        location = Point(float(self.request.GET['lat']), float(self.request.GET['lon']))
        context['location'] = location
        if self.request.POST:
            context['photo_form'] = PhotoForm(self.request.POST, self.request.FILES)
        else:
            context['photo_form'] = PhotoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = self.request.user
        form.instance.location = context['location']
        photo_form = context['photo_form']
        if photo_form.is_valid() and form.is_valid():
            photo = photo_form.save()
            self.object = form.save(commit=False)
            self.object.photo = photo
            self.object.save()
            return super(POICreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class POIDetailView(DetailView):
    queryset = POI.objects.all()

    def get_context_data(self, **kwargs):
        context = super(POIDetailView, self).get_context_data(**kwargs)
        context['is_owner'] = self.request.user == context['poi'].user
        return context


class POIUpdateView(UpdateView):
    model = POI
    form_class = POIForm
    queryset = POI.objects.all()
    template_name_suffix = '_update_form'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(POIUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(POIUpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.request.POST:
            context['photo_form'] = PhotoUpdateForm(self.request.POST,
                self.request.FILES, instance=self.object.photo)
        else:
            context['photo_form'] = PhotoUpdateForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = context['user']
        photo_form = context['photo_form']
        if photo_form.is_valid() and form.is_valid():
            photo = photo_form.save()
            self.object = form.save(commit=False)
            self.object.photo = photo
            self.object.save()
            return super(POIUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class POIDeleteView(DeleteView):
    model = POI
    queryset = POI.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(POIDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.username})

    def get_queryset(self):
        qs = super(POIDeleteView, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProfileCreateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.request.POST:
            context['photo_form'] = PhotoForm(self.request.POST, self.request.FILES)
        else:
            context['photo_form'] = PhotoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = context['user']
        photo_form = context['photo_form']
        if photo_form.is_valid() and form.is_valid():
            photo = photo_form.save()
            self.object = form.save(commit=False)
            self.object.photo = photo
            self.object.save()
            return super(UserProfileCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class UserProfileDetailView(DetailView):
    queryset = UserProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['is_owner'] = self.request.user == context['userprofile'].user
        return context


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    queryset = UserProfile.objects.all()
    template_name_suffix = '_update_form'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.request.POST:
            context['photo_form'] = PhotoForm(self.request.POST, self.request.FILES)
        else:
            context['photo_form'] = PhotoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = context['user']
        photo_form = context['photo_form']
        if photo_form.is_valid() and form.is_valid():
            photo = photo_form.save()
            self.object = form.save(commit=False)
            self.object.photo = photo
            self.object.save()
            return super(UserProfileUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))