import json
import re
from django.contrib.staticfiles import finders

'''
Functions relating to how strings are displayed
'''

# Add to this string if more types of delimiters are found
delimiters = r'[ _,|;"]+'


# Expects a path to the file we store string mappings and the actual string itself
def add_new_string_to_map_file(path, string_list):
    # Read the JSON into the buffer
    with open(path, 'r') as map_file:
        map_obj = json.load(map_file)

    tmp = map_obj

    for string in string_list:
        display_string = strip_and_capitalize(string)

        # Eg. {'hello_world': 'Hello World'}
        map_obj[string] = display_string
        # Also do the opposite for easier access {'Hello World': 'hello_world'}
        map_obj[display_string] = string

    # Overwrite the old JSON with the new one
    with open(path, 'w') as map_file:
        json.dump(map_obj, map_file)


def strip_and_capitalize(string):
    # Split up the string, capitalize, and join
    display_string_list = re.split(delimiters, string)
    display_string_list = [x.capitalize() for x in display_string_list]
    display_string = ' '.join(display_string_list)

    return display_string


# Gets list of display strings as their property names
# Try not to use this function for lists of small lengths (opening/closing files takes time!)
def convert_display_strings(path, string_list):
    property_name_list = []

    with open(path, 'r') as map_file:
        map_obj = json.load(map_file)
        for string in string_list:
            property_name_list.append(map_obj[string])

    return property_name_list


# Cache the dict in the app context so we don't have to use file i/o that often
def cache_display_strings(path, context):
    with open(path, 'r') as map_file:
        map_obj = json.load(map_file)

    context['display_string'] = map_obj


def write_cache_to_file(path, context):
    if 'display_string' not in context:
        Exception('No existing string display dictionary cached!')

    with open(path, 'w') as map_file:
        json.dump(context['display_string'], map_file)


def get_strings_from_cache(string_list, context):
    strings_to_update_json = []
    display_strings = []

    for string in string_list:
        # We're using _meta from Model, which will give a bunch of periods eg. Model.Table.columnproperty
        # Since we only want columnproperty, split & select the last part.
        column_name = str(string).rsplit('.', 1)[-1]
        if column_name not in context['display_string']:
            strings_to_update_json.append(column_name)
            display_strings.append(strip_and_capitalize(column_name))
        else:
            display_strings.append(context['display_string'][column_name])

    # if this isn't empty remember to update our json for next app startup
    if strings_to_update_json:
        path = finders.find('string_conversion.json')
        add_new_string_to_map_file(path, strings_to_update_json)
        cache_display_strings(path, context)

    return display_strings

