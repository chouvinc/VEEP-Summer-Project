from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.staticfiles import finders
from data_display.models import Students, Teams, Projects, NotForProfits
from data_display.utils import string_display

# TODO: There should be a native app context that Django offers. Store everything we store here there instead.
app_context = {'last_table': "", 'pagination_width': 2, 'last_data': [], 'last_headers': []}
# this will be changed via settings view in the future
RESULTS_PER_PAGE = 25


# Create your views here.
def database_start_page(request):
    # Add string display to our cache
    string_display.cache_display_strings(finders.find('string_conversion.json'), app_context)

    # Check for all the query parameters
    sort_by = request.GET.get('sort')
    page_number = request.GET.get('page')
    table = request.GET.get('table') or 'Students'

    if sort_by:
        data, table_headers = get_objects_by_table_and_sort(table,
                                                            string_display.get_strings_from_cache([sort_by],
                                                                                                  app_context)[0])
        app_context['last_data'], app_context['last_headers'] = data, table_headers
    elif not page_number or not app_context['last_data']:
        data, table_headers = get_objects_by_table(table)
        page_number = 1
        app_context['last_data'], app_context['last_headers'] = data, table_headers
    else:
        # This is the pagination case, just use the existing data.
        data, table_headers = app_context['last_data'], app_context['last_headers']

    table_headers = string_display.get_strings_from_cache(table_headers, app_context)

    # paginator is 1-based indexing (yikes)
    paginator = Paginator(data, RESULTS_PER_PAGE)
    subset_data = paginator.page(page_number)

    pages = get_pagination_ranges(paginator, int(page_number))
    return render(request, 'data_display/database_start_page.html',
                  {'data': subset_data, 'table_headers': table_headers,
                   'pages': pages}
                  )


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


def get_objects_by_table_and_sort(table_name, sort_by):
    return {
        'Students': (Students.objects.order_by(sort_by).values_list(), Students._meta.get_fields()),
        'Teams': (Teams.objects.order_by(sort_by).values_list(), Teams._meta.get_fields()),
        'Projects': (Projects.objects.order_by(sort_by).values_list(), Projects._meta.get_fields()),
        'Not For Profits': (NotForProfits.objects.order_by(sort_by).values_list(), NotForProfits._meta.get_fields())
    }[table_name]


def get_pagination_ranges(paginator, curr_page):
    total_pages = paginator.num_pages
    pages = {'left': [], 'right': [], 'current': curr_page}

    if curr_page - 1 > 1:
        pages['left'] = [curr_page - 2, curr_page - 1]
    if total_pages - curr_page > 1:
        pages['right'] = [curr_page + 1, curr_page + 2]

    return pages
