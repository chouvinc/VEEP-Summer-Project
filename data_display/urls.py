from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('', views.data_display, name="data_display"),
]