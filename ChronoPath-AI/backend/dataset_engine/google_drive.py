import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_credentials():

    creds = None

    # Existing authorization
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Refresh or create authorization
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        # Save authorization for future runs
        with open(
            "token.json",
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    return creds


def get_drive_service():

    credentials = get_credentials()

    return build(
        "drive",
        "v3",
        credentials=credentials
    )


def list_files(folder_id):

    service = get_drive_service()

    query = (
        f"'{folder_id}' in parents "
        "and trashed = false"
    )

    response = service.files().list(
        q=query,
        pageSize=100,
        fields=(
            "nextPageToken,"
            "files("
            "id,"
            "name,"
            "mimeType,"
            "size,"
            "modifiedTime"
            ")"
        )
    ).execute()

    return response.get(
        "files",
        []
    )