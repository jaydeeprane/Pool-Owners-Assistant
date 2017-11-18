from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

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
    one_day_later = today + datetime.timedelta(days=2)
    one_week_later = today + datetime.timedelta(weeks=1)
    print('Getting the upcoming events of next week')
    eventsResult = service.events().list(calendarId='primary', timeMin=one_day_later.isoformat() + 'Z',
                                         timeMax=one_week_later.isoformat() + 'Z',
                                         maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def add_event(service):
    event_to_add = {
        'summary': 'Dinner with friends',
        'description': 'Pizza served',
        'start': {
            'dateTime': '2017-11-18T09:00:00',
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': '2017-11-18T11:00:00',
            'timeZone': 'America/New_York'
        },
        'attendees': [
            {'email': 'akshit010292@gmail.com'}
        ]
    }
    event = service.events().insert(calendarId='primary', body=event_to_add).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def main():
    # Shows basic usage of the Google Calendar API.

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    getUpcomingEvents(service)

    # add_event(service)


if __name__ == '__main__':
    main()
