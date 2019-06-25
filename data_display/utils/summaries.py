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
    
    data_frame = pandas.DataFrame(data, None, table_headers)
    summary = data_frame.describe(include=include)
    
    return summary