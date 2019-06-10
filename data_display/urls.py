from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('settings', views.settings, name="settings"),
    path('', views.data_display, name="data_display"),
    path('import_export', views.import_export, name='import_export'),
    path('import_export/<i_form>', views.import_export, name='import_export'),
    path('import_export/<e_form>', views.import_export, name='import_export'),
    path('import_select', views.import_select, name='import_select'),
    path('import_intersection', views.import_intersection, name='import_intersection'),
    path('import_export_preview', views.import_export_preview, name='import_export_preview'),
    path('export_data', views.export_data, name='export_data')
]