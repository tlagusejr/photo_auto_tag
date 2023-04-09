'''Photo app generic views'''

from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Photo

import base64
import json

import requests

from urllib.parse import unquote


class PhotoListView(ListView):
    model = Photo

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/taglist.html'

    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo

    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')


def PhotoClassifyView(request,pk):

    api = '#http://11.11.11.11:57340/api'
    model = Photo
    image_obj = model.objects.get(pk=pk)
    image_url = unquote(image_obj.image.url)
    image_file = "/Users/hdsim/Django-photo-app/config" + image_url

    def image_classify(image_file,image_obj):
        with open(image_file, "rb") as f:
            im_bytes = f.read()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps({"image": im_b64, "other_key": "value"})
        print(f"이미지 전송 {image_file}")
        response = requests.post(api, data=payload, headers=headers)
        try:
            data = response.json()
            image_obj.tags.add(data['class'])
            image_obj.save()

        except requests.exceptions.RequestException:
            print(response.text)

    image_classify(image_file,image_obj)
    return redirect('photo:list')