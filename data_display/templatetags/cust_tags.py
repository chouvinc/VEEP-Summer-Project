from django import template
register = template.Library()

@register.filter
def index(List, i):
    """this function will allow us to index the list of data we have in our template to display the 
    data in teh proper table format"""
    return List[int(i)]

