from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import HoverTool
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response
from django.contrib.staticfiles import finders
from data_display.models import Students, Teams, Projects, NotForProfits
from data_display.utils import string_display
from data_display.forms import QueryTable, SettingsForm
from veep_data_project.settings import rows_per_page

# TODO: There should be a native app context that Django offers. Store everything we store here there instead.
app_context = {'last_table': "", 'last_filter': "", 'pagination_width': 2, 'last_data': [], 'last_headers': [], 'last_sort': '',
               'ui_obj': {'asc': '', 'desc': ''}}
FIRST = True

def settings(request):
    if request.method == "GET":
        form = SettingsForm(request.GET)
        if form.is_valid():
            global rows_per_page
            rows_per_page = form.cleaned_data['rows_per_page']
    else:
        form = SettingsForm()
    return render(request, 'data_display/settings.html', {'form':form})


# Create your views here.
def visualizations(request):
    x = [4,5]
    y = [2,6]
    plot = figure(title = 'Project Graph',
                  x_axis_label='X', y_axis_label='Y',
                  plot_width =400, plot_height=400)
    plot.line(x, y, line_width=2)
    script, div = components(plot)
    return render(request,'data_display/visualizations.html', {'script' : script, 'div' : div})

def data_display(request):

    # Add string display to our cache
    string_display.cache_display_strings(finders.find('string_conversion.json'), app_context)

    # Request params
    sort_by = request.GET.get('sort_by')
    page_number = request.GET.get('page') or 1
    page_number = int(page_number)
    table = request.GET.get('table') or app_context['last_table'] or 'Students'

    if request.method == "GET" and request.GET.get('table'):
        form = QueryTable(request.GET)
        if form.is_valid():
            table = form.cleaned_data['table']
            filter = form.cleaned_data['filter']
            app_context['last_table'] = table
            app_context['last_filter'] = filter
    else:
        use_old_table = {'filter': app_context['last_filter'],
                         'table': app_context['last_table']}
        form = QueryTable(use_old_table)

    if page_number != 1:
        # pagination case, just use existing data
        data, table_headers = app_context['last_data'], app_context['last_headers']
    elif sort_by:
        sort_by = toggle_sort(sort_by, app_context)
        data, table_headers = get_objects_by_table_and_sort(table, sort_by)
        app_context['last_data'], app_context['last_headers'] = data, table_headers
    else:
        # first visit, no sorting
        data, table_headers = get_objects_by_table(table)
        app_context['last_data'], app_context['last_headers'] = data, table_headers

    # Fix table headers to display values
    table_headers = string_display.get_strings_from_cache(table_headers, app_context)

    # paginator is 1-based indexing (yikes)
    paginator = Paginator(data, rows_per_page)
    pages = get_pagination_ranges(paginator, page_number)
    subset_data = paginator.page(page_number)

    return render(
        request, 'data_display/database_start_page.html',
        {'data': subset_data, 'table_headers': table_headers, 'pages': pages, 'ui': app_context['ui_obj'], 'form': form}
    )


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


def toggle_sort(sort_by, context):
    asc_sort = string_display.get_strings_from_cache([sort_by], context)[0]
    if context['last_sort'] == asc_sort:
        # already sorted this column -- toggle so desc
        desc_sort = '-' + asc_sort
        context['last_sort'] = desc_sort
        context['ui_obj']['desc'] = sort_by
        context['ui_obj']['asc'] = ''
        return desc_sort
    else:
        # first time we sort, or previous was desc (in which case column doesn't match), do nothing
        context['last_sort'] = asc_sort
        context['ui_obj']['asc'] = sort_by
        context['ui_obj']['desc'] = ''
        return asc_sort
