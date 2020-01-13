from datetime import datetime
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask import current_app as app

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly',
]

_service = None
def create_service():
    global _service

    if _service is not None:
        return _service

    account_json = app.config['GOOGLE_SERVICE_ACCOUNT_JSON']
    if account_json is not None:
        account_data = json.loads(account_json)
        creds = service_account.Credentials.from_service_account_info(
            account_data, scopes=SCOPES,
        )
        _service = build('calendar', 'v3', credentials=creds)
        return _service
    else:
        print('$GOOGLE_SERVICE_ACCOUNT_JSON not set. '
              'Calendar events access is disabled', file=sys.stderr)
        return None

def list_events(*, num=None, since=None):
    service = create_service()
    if service is None:
        return None

    calendarId = app.config['GOOGLE_CALENDAR_ID']
    if calendarId is None:
        print('$GOOGLE_CALENDAR_ID not set. Ignoring.', file=sys.stderr)
        return None

    if since is None:
        since = datetime.utcnow().isoformat() + 'Z'

    result = service.events().list(
        calendarId=calendarId,
        timeMin=since,
        maxResults=num,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return result['items']
