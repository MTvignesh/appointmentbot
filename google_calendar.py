from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def check_availability(date: str, start_time: str, end_time: str) -> bool:
    service = get_calendar_service()
    start = f"{date}T{start_time}:00+05:30"
    end = f"{date}T{end_time}:00+05:30"

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return len(events_result.get('items', [])) == 0

def book_event(date: str, start_time: str, end_time: str, summary: str):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {
            'dateTime': f"{date}T{start_time}:00+05:30",
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': f"{date}T{end_time}:00+05:30",
            'timeZone': 'Asia/Kolkata',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return {
        "id": created_event.get("id"),
        "start": created_event["start"]["dateTime"],
        "end": created_event["end"]["dateTime"]
    }
