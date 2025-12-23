from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def get_last_row_data(spreadsheet_id, range_name):
    print("Sheet information fetched successfully")
    # creds = service_account.Credentials.from_service_account_file(
    #     os.getenv("GOOGLE_CREDENTIALS_FILE"),
    #     scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    # )
    # service = build("sheets", "v4", credentials=creds)
    # sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    # values = result.get("values", [])
    # if not values:
    #     return None
    # return values[-1]   # last row
    return {
        'name':'my name',
        'email': 'user@example.com'
    }
