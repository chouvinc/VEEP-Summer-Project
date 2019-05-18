import json
import re

'''
Functions relating to how strings are displayed
'''

# Add to this string if more types of delimiters are found
delimiters = r'[ _,|;"]+'


# Expects a path to the file we store string mappings and the actual string itself
def add_new_string_to_map_file(path, string):
    # Split up the string, capitalize, and join
    display_string_list = re.split(delimiters, string)
    display_string_list = [x.capitalize() for x in display_string_list]
    display_string = ' '.join(display_string_list)

    # Read the JSON into the buffer
    with open(path, 'r') as map_file:
        map_obj = json.load(map_file)

    tmp = map_obj
    # Eg. {'hello_world': 'Hello World'}
    map_obj[string] = display_string
    # Also do the opposite for easier access {'Hello World': 'hello_world'}
    map_obj[display_string] = string

    # Overwrite the old JSON with the new one
    with open(path, 'w') as map_file:
        json.dump(map_obj, map_file)


# Gets list of display strings as their property names
# Try not to use this function for lists of small lengths (opening/closing files takes time!)
def convert_display_strings(path, string_list):
    property_name_list = []

    with open(path, 'r') as map_file:
        map_obj = json.load(map_file)
        for string in string_list:
            property_name_list.append(map_obj[string])

    return property_name_list
