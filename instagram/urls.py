from django.conf.urls import url
from . import views

app_name = "instagram"

urlpatterns = [
    url('', views.InstagramPhotoListView.as_view(), name="list_view"),
]
