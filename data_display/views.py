from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles import finders
from data_display.models import Students
from data_display.utils import string_display, dummy_data

# TODO: There should be a native app context that Django offers. Store everything we store here there instead.
app_context = {}


# Create your views here.
def database_start_page(request):
    # TODO: delete this
    # Run this for UI testing (set 'test' to True)
    example = {
    'student_id': [1005243844, 10067329845, 1009289304, 1009283681, 1002736541, 1009872837, 1008227736, 1009988374, 1002938823, 1001010267], 
    'name': ['Bushi Dokaj', 'Peter Parker', 'Susan Summer', 'Leif Hebel', 'Carita Stringfellow', 'Ronny Newhouse', 'Chris Charis', 'Carlton Cockrum', 'Willy Hutchins','Orval Cooks'],  
    'discipline': ['Industrial','Mech','Mech','ECE', 'ECE','Industrial', 'Mech', 'Chem', 'ECE','ECE'],
    'year': ['2T2', '2T1', '1T9','1T9','2T0','1T9','2T1','2T1', '1T9','1T9'],
    'project':['VEEP Database Imporvement', '180 DC', '180 DC', 'VEEP Database Imprpvement', 'Lighthouse Labs', 'Lighthouse Labs', 'TPVH', 'TPVH', 'TPVH', 'Brands for Canada']
    }

    # Add string display to our cache
    string_display.cache_display_strings(finders.find('string_conversion.json'), app_context)

    # Setting up using models to generate table data instead
    students = Students.objects.values_list()
    table_headers = string_display.get_strings_from_cache(Students._meta.get_fields(), app_context)

    return render(request, 'data_display/database_start_page.html', {'example':example, 'test': False, 'data': students, 'table_headers': table_headers})


def display_data(request):

    # table = request.GET.get('tables')
    # filter_table = request.GET.get('filter')

    return render(request, 'data_display/database_start_page.html', {'example': example})
