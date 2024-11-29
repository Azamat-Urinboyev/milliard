from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging



class Sheets:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id

    def _create_service(self):
        SERVICE_ACCOUNT_FILE = 'config/credentials.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service


    def _get_last_row(self, service, table_name):
        last_row = len(service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=f"{table_name}!A:A").execute()["values"])
        return last_row


    def update_calls(self, table_name, calls):
        calls_num = len(calls)
        service = self._create_service()
        last_occupied_row = self._get_last_row(service=service, table_name=table_name)
        value_input_option = "USER_ENTERED"

        try:
            service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f"{table_name}!A{last_occupied_row+1}:I{last_occupied_row+calls_num+1}",
                valueInputOption=value_input_option,
                body={"values": calls}
            ).execute()
        except Exception as e:
            logging.error(e)
        

    def update_attendance(self, table_name, attendance):
        attendance_num = len(attendance)
        service = self._create_service()
        last_occupied_row = self._get_last_row(service=service, table_name=table_name)
        value_input_option = "USER_ENTERED"

        try:
            service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f"{table_name}!A{last_occupied_row+1}:I{last_occupied_row+attendance_num+1}",
                valueInputOption=value_input_option,
                body={"values": attendance}
            ).execute()
        except Exception as e:
            logging.error(e)
            