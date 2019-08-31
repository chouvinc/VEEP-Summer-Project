from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components
from bokeh.models import LabelSet, ColumnDataSource
from bokeh import palettes
import math
from django.db.models import Count
from data_display.models import get_model_from_name
import pandas

#Plotting Functions:
def line(x, y, x_label, y_label, line_color, line_width):
    plot = figure(x_range = x,
                  title = y_label + ' vs. ' + x_label,
                  plot_width = 600,
                  plot_height = 600)
    plot.line(x, y,
              line_color = line_color,
              line_width = line_width)
    plot.xaxis.axis_label = x_label
    plot.yaxis.axis_label = y_label
    return components(plot)

def circle(x, y, x_label, y_label):
    plot = figure(x_range = x,
                  title = y_label + ' vs. ' + x_label,
                  plot_width = 600,
                  plot_height = 600)
    plot.circle(x, y,
              color = 'grey',
              fill_alpha = 0.2,
              size = 10)
    plot.xaxis.axis_label = x_label
    plot.yaxis.axis_label = y_label
    return components(plot)

def bar(x, y, x_label, y_label,bar_width):
    plot = figure(x_range = x,
                  title = y_label + ' vs. ' + x_label,
                  plot_width = 600,
                  plot_height = 600)
    plot.vbar(x = x, top = y, width = bar_width, color = palettes.magma(len(x)))
    return components(plot)

def wedge(data, title):
    data = pandas.Series (data).reset_index(name='value').rename(columns={'index':'data'+'List'})
    data['angle'] = data['value'] / data['value'].sum()*2*math.pi
    data['color'] = palettes.viridis(len(data))
    plot = figure(title = title,
                  plot_width = 600,
                  plot_height = 600,
                  tools = 'hover',
                  tooltips = "@dataList: @value" ,
                  x_range = (-0.5, 1))
    plot.wedge(x = 0, y = 1, radius = 0.4,
               start_angle = cumsum('angle', include_zero = True), end_angle = cumsum('angle'),
               line_color = 'white',
               fill_color = 'color',
               legend = 'dataList',
               source = data)

    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    return components(plot)


#Getting Data Functions:

def get_distinct(model, field):
    #get the model
    MODEL = get_model_from_name(model)

    #get a queryset of the disctinct values in the field of the model i.e <'year': 1, 'year':2, 'year':3 ...>
    qs = MODEL.objects.values_list(field,flat=True).distinct().order_by(field)

    #get the data list, Bokeh plot.line() function can only process input in list form [1,2,3...]
    distinct = list(qs)
    return distinct

def count_by(model, field):
    #get the model
    MODEL = get_model_from_name(model)

    #get a queryset contains the distinct field values and their individual count
    qs1_count = MODEL.objects.values(field).annotate(count=Count(field,distinct=True))
    qs2 = MODEL.objects.values_list(field,flat=True).distinct().order_by(field)

    #Use union to ensure the field values with count 0 still are kept, TODO: check the output
    qs2.union(qs1_count).order_by(field)
    return qs2

##TODO: complete the fucntion that returns the same type of dataset as student_disciplines
###student_disciplines ={'EngSci':3,'TrackOne':7,'Chem':4,'Civ':1,'ECE':5,'Indy':8,'Material':2,'Mech':4,'Min':1}
def get_wedge_data(model,field):
    return 0
