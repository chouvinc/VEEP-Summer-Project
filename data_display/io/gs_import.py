import pickle
import os.path
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib.staticfiles import finders
import data_display.utils.constants as constants
from data_display.utils.string_display import get_strings_from_cache
from fuzzywuzzy import fuzz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

# CREDENTIALS LOCATION
CREDENTIALS_PATH = finders.find('credentials.json')


def choose_import_type(import_type):
    return {
        constants.INDEPENDENT: independent_import,
        constants.INTERSECTION: intersection_import,
        constants.UNION: union_import,
        constants.MAP: map_import
    }[import_type]


def independent_import():
    pass


def intersection_import(new_data, existing_model, app_context):
    # Get the last n entries from our old table (to be first half of diff view)
    last_n = existing_model.objects.all().order_by('-id').values_list()[:50]

    # Get the headers of both sets of data
    existing_model_headers = get_strings_from_cache(existing_model._meta.get_fields(), app_context)
    new_model_headers = new_data[0]

    print(len(new_data))
    print(len(new_data[0]))

    list_len = len(new_data[0])

    # for i in range(list_len):
    #     # list isn't sorted, best we can do is O(n^2)
    #     for old_header in existing_model_headers:
    #         # append '-' to the header to designate deletion on the UI if headers don't match fuzzy ratio
    #         # for more information on fuzzywuzzy see: https://stackoverflow.com/questions/10383044/fuzzy-string-comparison
    #         if fuzz.partial_ratio(new_data[0][i], old_header) > 90:
    #             print(new_data[0][i])
    #         else:
    #             delete_column(new_data, i)
    #             # now check if we're about to go over the length
    #             if i >= len(new_data) - 1:
    #                 break

    # Return the new data (show the end of the old data and the part of the new inserted data)
    return new_data[1::], new_model_headers


def delete_column(arr, index):
    for row in arr:
        del row[index]


def union_import():
    pass


def map_import():
    pass


def get_data_from(url):
    gsheet_id = validate_url(_get_id_from_url(url))
    creds = validate_login()

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    sheet_metadata = service.spreadsheets().get(spreadsheetId=gsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    title = sheets[0].get("properties", {}).get("title", "Sheet1")

    # Note that 'title' only returns the non-indexed version of the form. Google forms will often
    # append indices to sheet names because it's automated, so adding the 1 works here.
    # TODO: WARNING: THIS COULD BE A BUG IN THE FUTURE IF WE EXTEND FUNCTIONALITY TO ALLOW CUSTOM SHEETS
    result = sheet.values().get(spreadsheetId=gsheet_id,
                                range=title).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values


def validate_url(id_match):
    if not id_match:
        raise KeyError('Not a google sheet url!')
    else:
        return id_match.group(0)


# some copy pasta from google sheets API
def validate_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def _get_id_from_url(url):
    return re.search('[-\w]{25,}', url)


# Test script copied from quick start
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    main()