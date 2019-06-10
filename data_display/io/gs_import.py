import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib.staticfiles import finders
import data_display.utils.constants as constants
from data_display.utils.string_display import get_strings_from_cache

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
    # Check which columns match exactly, then infer the data

    # Return the new data (show the end of the old data and the part of the new inserted data)
    last_n = existing_model.objects.all().order_by('-id').values_list()[:50]
    return reversed(last_n), get_strings_from_cache(existing_model._meta.get_fields(), app_context)


def union_import():
    pass


def map_import():
    pass


def get_data_from(url):
    pass


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