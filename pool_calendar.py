from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

import holidays

nc_holidays = holidays.UnitedStates(state='NC', years=2017)
pool_suggestion_key_list = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0]
pool_suggestion_key = {
    "New Year's Day": True,
    "New Year's Day (Observed)": False,
    "Martin Luther King, Jr. Day": False,
    "Washington's Birthday": False,
    "Good Friday": True,
    "Memorial Day": False,
    "Independence Day": True,
    "Labor Day": False,
    "Columbus Day": False,
    "Veterans Day (Observed)": False,
    "Veterans Day": False,
    "Thanksgiving": True,
    "Day After Thanksgiving": False,
    "Christmas Eve (Observed)": True,
    "Christmas Eve": False,
    "Christmas Day": True,
    "Day After Christmas": False,
}

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-pool.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_pool.json'
APPLICATION_NAME = 'Pool Owner Assistant'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-pool.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getUpcomingEvents(service):
    # Creates a Google Calendar API service object and outputs a list of the next 10 events on the user's calendar.

    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    today = datetime.datetime.today()
    two_day_later = today + datetime.timedelta(days=2)
    one_week_later = today + datetime.timedelta(weeks=1)
    print('Getting the upcoming events of next week')
    eventsResult = service.events().list(calendarId='primary', timeMin=two_day_later.isoformat() + 'Z',
                                         timeMax=one_week_later.isoformat() + 'Z',
                                         maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def add_event(service):
    today = datetime.datetime.today()
    start_time = today + datetime.timedelta(hours=24)
    end_time = start_time + datetime.timedelta(hours=3)
    event_to_add = {
        'summary': 'Pool Party',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'America/New_York'
        }
        # ,
        # 'attendees': [
        #     {'email': 'akshit010292@gmail.com'}
        # ]
    }
    event = service.events().insert(calendarId='primary', body=event_to_add).execute()
    # print('Event created: %s' % (event.get('htmlLink')))


def suggest_party():
    # today = datetime.datetime.today()
    today = datetime.datetime(2017, 12, 19)
    two_day_later = today + datetime.timedelta(days=2)
    holiday_name = nc_holidays.get(two_day_later.date())
    if holiday_name is None:
        return False
    elif pool_suggestion_key[holiday_name]:
        return two_day_later, holiday_name
    else:
        return False


# Shows basic usage of the Google Calendar API.

# credentials = get_credentials()
# http = credentials.authorize(httplib2.Http())
# service = discovery.build('calendar', 'v3', http=http)

# getUpcomingEvents(service)

# add_event(service)

# print (suggest_party())
