from django.views.generic import ListView
from django.shortcuts import render
from .models import InstagramPhoto
from .utils import crawl_instagram_profile


class InstagramPhotoListView(ListView):
    template_name = 'instagram/list_view.html'
    model = InstagramPhoto

    def get_context_data(self, *args, **kwargs):
        something = crawl_instagram_profile()
        return super(InstagramPhotoListView, self).get_context_data(*args, **kwargs)