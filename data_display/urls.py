from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('', views.data_display, name="data_display"),
    path('settings', views.settings, name="settings"),
    path('import_export', views.import_export, name='import_export'),
    path('import_export/<i_form>', views.import_export, name='import_export'),
    path('import_export/<e_form>', views.import_export, name='import_export'),
    # We need this 3rd path because django treats optional parameters in a view function as positional args on
    # redirect. TODO: figure out a way that doesn't make this so confusing!
    path('import_export/<i_form>/<e_form>', views.import_export, name='import_export'),
    path('import_select', views.import_select, name='import_select'),
    path('import_intersection', views.import_intersection, name='import_intersection'),
    path('import_export_preview', views.import_export_preview, name='import_export_preview'),
    path('export_select', views.export_select, name='export_select'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('summaries', views.summaries, name = "summaries")
]