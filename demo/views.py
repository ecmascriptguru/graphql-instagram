from django.views.generic import ListView
from django.shortcuts import render
from .models import InstagramPhoto

# Create your views here.

class DemoListView(ListView):
    template_name = 'demo/demo_list_view.html'
    model = InstagramPhoto