from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('', views.database_start_page, name='database_start_page'),
    path('', views.display_data, name="display_data"),
    path('summaries/', views.summaries, name="summaries")
]