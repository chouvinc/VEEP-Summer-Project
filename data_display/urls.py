from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('database', views.data_display, name='data_display'),
    path('settings', views.settings, name = "settings" )
]