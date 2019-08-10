from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from data_display.models import Students, Teams, Projects, NotForProfits, get_model_from_name
from data_display.utils import string_display
from veep_data_project.settings import rows_per_page
from data_display.utils.summaries import perf_indicator, get_data
from data_display.forms import QueryTable, SettingsForm, SummariesForm, ImportSelectForm, ExportSelectForm, \
    IntersectionImportForm, ConfirmThingForm, \
    get_import_form_from_type, get_export_form_from_type

from django.contrib import messages
from data_display.utils.constants import ISELECT, ESELECT
from data_display.io import gs_import
import pandas 

# TODO: There should be a native app context that Django offers. Store everything we store here there instead.
# also this is a terrible practice and I'm sorry for anyone who has to read this =(
app_context = {'last_table': "", 'last_filter': "", 'pagination_width': 2, 'last_data': [], 'last_headers': [],
               'last_sort': '', 'ui_obj': {'asc': '', 'desc': ''}, 'preview_data': [], 'display_string': {},
               'model': None}
# this will be changed via settings view in the future
RESULTS_PER_PAGE = 25


def summaries(request):
    table_name = "Students"
    tables = ["Students", "Projects", "Not For Profits", "Teams"]
    if request.method == "GET":
        form = SummariesForm(request.GET)
        if form.is_valid():
            table_name = form.cleaned_data['table']
    else:
        form = SummariesForm()
    
    data, table_headers = get_data(table_name)
    data_frame = pandas.DataFrame(data, None, table_headers)
    summary = data_frame.describe(include='all')
    summary = summary.fillna("")

    kpi = perf_indicator(tables)
    kpi = pandas.DataFrame.from_dict(kpi)

    return render(request, 'data_display/summary.html', {'form':form, 'summary':summary.to_html(), 
    'kpi':kpi.to_html(index=None)})

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


def import_export(request, i_form=ISELECT, e_form=ESELECT):
    selected_i_form = get_import_form_from_type(i_form)
    selected_e_form = get_export_form_from_type(e_form)
    return render(request, 'data_display/import_export.html',
                  {
                      'i_form': selected_i_form, 'i_form_type': selected_i_form.form_type,
                      'e_form': selected_e_form
                  })


def import_export_preview(request):
    subset_data, table_headers, old_data, old_headers = app_context['preview_data']

    if request.method == 'POST':
        confirm_form = ConfirmThingForm(request.POST)
        if confirm_form.is_valid() and confirm_form.cleaned_data['confirmed']:
            gs_import.append_records_to_existing_table(app_context['model'], subset_data, table_headers, app_context)
            messages.success(request, 'Added new data to table')
            return redirect('import_export')
    else:
        confirm_form = ConfirmThingForm(request.POST)

    return render(request, 'data_display/import_diff.html', {'data': subset_data, 'table_headers': table_headers,
                                                             'old_data': old_data, 'old_headers': old_headers,
                                                             'form': confirm_form})


# === io form processing ===
def import_select(request):
    if request.method == "POST":
        form = ImportSelectForm(request.POST)
        if form.is_valid():
            return redirect('import_export', i_form=form.cleaned_data['import_type'])
    return redirect('import_export', i_form=ISELECT)


def import_intersection(request):
    if request.method == "POST":
        form = IntersectionImportForm(request.POST)
        if form.is_valid():
            selected_model = get_model_from_name(form.cleaned_data['existing_table'])
            form_type = form.form_type
            gsheet_url = form.cleaned_data['url']

            # first get the new data
            new_data = gs_import.get_data_from(gsheet_url)

            # then process the data according to gs_import
            intersect_import = gs_import.choose_import_type(form_type)

            # save the preview data to the app context, remember the model
            app_context['preview_data'] = intersect_import(new_data, selected_model, app_context)
            app_context['model'] = selected_model

            return redirect('import_export_preview')
        else:
            print(form.errors)
    return redirect('import_export', i_form=ISELECT)


def import_data(request):
    if request.method == "POST":
        pass
    else:
        pass

    return redirect('import_export')


def export_data(request):
    if request.method == "GET":
        pass
    else:
        pass

    return redirect('import_export')


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
