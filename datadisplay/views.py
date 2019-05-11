from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def database_start_page(request): 

    example = {
    'student_id': [1005243844, 10067329845, 1009289304, 1009283681, 1002736541, 1009872837, 1008227736, 1009988374, 1002938823, 1001010267], 
    'name': ['Bushi Dokaj', 'Peter Parker', 'Susan Summer', 'Leif Hebel', 'Carita Stringfellow', 'Ronny Newhouse', 'Chris Charis', 'Carlton Cockrum', 'Willy Hutchins','Orval Cooks'],  
    'discipline': ['Industrial','Mech','Mech','ECE', 'ECE','Industrial', 'Mech', 'Chem', 'ECE','ECE'],
    'year': ['2T2', '2T1', '1T9','1T9','2T0','1T9','2T1','2T1', '1T9','1T9'],
    'project':['VEEP Database Imporvement', '180 DC', '180 DC', 'VEEP Database Imprpvement', 'Lighthouse Labs', 'Lighthouse Labs', 'TPVH', 'TPVH', 'TPVH', 'Brands for Canada']
    }
    
    return render(request, 'datadisplay/database_start_page.html', {'example':example})

def display_data(request):
   
    # table = request.GET.get('tables')
    # filter_table = request.GET.get('filter')

    return render(request, 'datadisplay/database_start_page.html', {'example':example})
