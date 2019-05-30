from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.staticfiles import finders
from data_display.models import Students, Teams, Projects, NotForProfits
from data_display.utils import string_display, dummy_data

# TODO: There should be a native app context that Django offers. Store everything we store here there instead.
app_context = {'existing_query_params': "Students"}
# this will be changed via settings view in the future
RESULTS_PER_PAGE = 10


# Create your views here.
def database_start_page(request):
    # Add string display to our cache
    string_display.cache_display_strings(finders.find('string_conversion.json'), app_context)

    # Setting up using models to generate table data instead, defaulting to Students
    # TODO: replace query parameters with django form data, will make pagination logic less confusing
    # TODO: remove additional or existing query params after django forms
    existing_query_params = app_context['existing_query_params']
    new_query_params = request.GET.get('tables') or existing_query_params

    data, table_headers = get_objects_by_table(new_query_params)

    app_context['existing_query_params'] = new_query_params
    table_headers = string_display.get_strings_from_cache(table_headers, app_context)

    # paginator is 1-based indexing (yikes)
    page_number = request.GET.get('page') or 1
    paginator = Paginator(data, RESULTS_PER_PAGE)

    subset_data = paginator.page(page_number)

    return render(request, 'data_display/database_start_page.html',
                  {'data': subset_data, 'table_headers': table_headers})


def display_data(request):
    # table = request.GET.get('tables')
    # filter_table = request.GET.get('filter')

    return render(request, 'data_display/database_start_page.html', {'example': example})


# Should move this to a model-layer module (this is the resource layer)
def get_objects_by_table(table_name):
    return {
        'Students': (Students.objects.values_list(), Students._meta.get_fields()),
        'Teams': (Teams.objects.values_list(), Teams._meta.get_fields()),
        'Projects': (Projects.objects.values_list(), Projects._meta.get_fields()),
        'Not For Profits': (NotForProfits.objects.values_list(), NotForProfits._meta.get_fields())
    }[table_name]
