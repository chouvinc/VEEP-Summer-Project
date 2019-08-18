from data_display.utils import string_display
from django.contrib.staticfiles import finders
from data_display.models import Students, Teams, Projects, NotForProfits
import pandas

app_context = {'last_table': "", 'last_filter': "", 'pagination_width': 2, 'last_data': [], 'last_headers': [], 'last_sort': '',
               'ui_obj': {'asc': '', 'desc': ''}}

def get_objects_by_table(table_name):
    return {
        'Students': (Students.objects.values_list(), Students._meta.get_fields()),
        'Teams': (Teams.objects.values_list(), Teams._meta.get_fields()),
        'Projects': (Projects.objects.values_list(), Projects._meta.get_fields()),
        'Not For Profits': (NotForProfits.objects.values_list(), NotForProfits._meta.get_fields())
    }[table_name]

def get_data(table_name):
    string_display.cache_display_strings(finders.find('string_conversion.json'), app_context)
    
    include = ['object', 'int', 'float']
    
    data, table_headers = get_objects_by_table(table_name)
    app_context['last_data'], app_context['last_headers'] = data, table_headers
    table_headers = string_display.get_strings_from_cache(table_headers, app_context)
    
    return data, table_headers

def perf_indicator(table_names):
    KPI = {'Number of Successful Students': 0, 'Average Project Completion': 0,
    'Number of NFP\'s': 0, 'Number of Teams': 0}
    for name in table_names:
        data, table_headers = get_data(name)
        data_frame = pandas.DataFrame(data, None, table_headers)
        summary = data_frame.describe(include='all')
        if name == "Students":
            KPI['Number of Successful Students'] = [summary["Name"]["count"]]
        if name == "Projects":
            KPI["Average Project Completion"] = [summary["Completion Rate"]["mean"].round(0)]
        if name == "Not For Profits":
            KPI['Number of NFP\'s'] = [summary["Nfp Name"]["count"]]
        if name == "Teams":
            KPI['Number of Teams'] = [summary["Team Name"]["count"]]
    return KPI
