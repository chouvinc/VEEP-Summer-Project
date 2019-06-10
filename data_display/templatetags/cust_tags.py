from django import template
register = template.Library()

@register.filter
def is_valid(form):
    if form.is_valid():
        return True
    else:
        return False 
    

