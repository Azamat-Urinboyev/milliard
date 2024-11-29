from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import pandas as pd
from datetime import datetime, timedelta


class Reports:
    def __init__(self, info_file = "data/raw/sheets_info.json"):
        self.service = None
        self.sheets_info = None
        self.sheets_info_file = info_file

        self.load_sheets_info()
        self.create_service()

    def load_sheets_info(self):
        with open(self.sheets_info_file) as f:
            self.sheets_info = json.load(f)

    def create_service(self):
        SERVICE_ACCOUNT_FILE = 'config/credentials.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        self.service = service
    
    def get_calls(self):
        sheet_id = self.sheets_info["calls"]["sheet_id"]
        table_name = self.sheets_info["calls"]["table_name"]
        data_range = self.sheets_info["calls"]["range"]
        start_date = self.sheets_info["calls"]["start_date_cell"]
        end_date = self.sheets_info["calls"]["end_date_cell"]

        value_input_option = "USER_ENTERED"

        #changing date
        today = datetime.now().strftime("%d.%m.%Y")
        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{start_date}",
            valueInputOption=value_input_option,
            body={"values": [[""]]}
            ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{end_date}",
            valueInputOption=value_input_option,
            body={"values": [[today]]}
            ).execute()
        
        #getting report from google sheets
        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        df = pd.DataFrame(data=data[1:], columns=data[0])
        data_to_sort = df.iloc[:-1]
        last_row = df.iloc[[-1]]
        data_to_sort.loc[:, "исходящий"] = data_to_sort["исходящий"].astype(str).astype(int)
        sorted_df = data_to_sort.sort_values(by="исходящий", ascending=False)
        df = pd.concat([sorted_df, last_row])
        df = df.set_index(df.columns[0])
        return df


    def get_productivity(self):
        sheet_id = self.sheets_info["productivity"]["sheet_id"]
        table_name = self.sheets_info["productivity"]["table_name"]
        data_range = self.sheets_info["productivity"]["range"]

        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        df = pd.DataFrame(data=data[1:], columns=data[0])
        main_data = df.iloc[:-1]
        last_row = df.iloc[[-1]]
        main_data.loc[:, "Унумдорлик"] = main_data["Унумдорлик"].astype(str).astype(int)
        main_data = main_data.sort_values(by="Унумдорлик")
        main_data["Рейтинг"] = range(1, len(main_data)+1)
        main_data["ranking_change"] = main_data.iloc[:, 0].astype(int) - main_data["Рейтинг"]
        main_data["Рейтинг ўзгариши"] = main_data["ranking_change"].apply(self._calculate_ranking)
        df = pd.concat([main_data, last_row])
        df = df[["Рейтинг", "Рейтинг ўзгариши", "Прогноз", "Сотув хозирги", "Ўзгариш 17-дастурга нисбатан", "Унумдорлик", "Қўшимча сотув прогнози", "Умумий сотув прогнози", "Бонус прогноз%"]]
        df = df.set_index(df.columns[0])
        df["Ўзгариш 17-дастурга нисбатан"] = df["Ўзгариш 17-дастурга нисбатан"].astype(int)
        return df


    def _calculate_ranking(self, rank_num):
        ranking = int(rank_num)
        resulting_ranking = ""
        if ranking > 0:
            resulting_ranking = f"⬆️ +{ranking}"
        elif ranking < 0:
            resulting_ranking = f"⬇️ {ranking}"
        else:
            resulting_ranking = f"➡️ ={ranking}"

        return resulting_ranking
    

    def get_call_time(self):
        sheet_id = self.sheets_info["call_time"]["sheet_id"]
        table_name = self.sheets_info["call_time"]["table_name"]
        data_range = self.sheets_info["call_time"]["range"]


        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]

        df = pd.DataFrame(data=data[1:], columns=data[0])
        main_data = df.iloc[:-1]
        last_row = df.iloc[[-1]]
        main_data.loc[:,"Время первого звонка"] = main_data.apply(lambda row: "zzz" if row["Пришел(а)"] == "_-_" else row["Время первого звонка"], axis=1)
        main_data = main_data.sort_values(by="Время первого звонка")
        main_data["Время первого звонка"] = main_data["Время первого звонка"].replace({"zzz": ""})
        df = pd.concat([main_data, last_row])
        df = df.set_index(df.columns[0])
        return df


    def get_lead_report(self):
        sheet_id = self.sheets_info["leads"]["sheet_id"]
        table_name = self.sheets_info["leads"]["table_name"]
        daily_range = self.sheets_info["leads"]["daily_range"]
        all_range = self.sheets_info["leads"]["all_range"]
        check_date = self.sheets_info["leads"]["check_date"]
        check_value = self.sheets_info["leads"]["check_value"]
        daily_set_date = self.sheets_info["leads"]["daily_set_date"]
        all_set_date = self.sheets_info["leads"]["all_set_date"]

        value_input_option = "USER_ENTERED"

        #changing date
        yesterday = datetime.now() - timedelta(days=1)
        yesterday = yesterday.strftime("%d.%m.%Y")

        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{check_date}",
            valueInputOption=value_input_option,
            body={"values": [[yesterday]]}
        ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{daily_set_date}",
            valueInputOption=value_input_option,
            body={"values": [[yesterday]]}
        ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{all_set_date}",
            valueInputOption=value_input_option,
            body={"values": [[yesterday]]}
        ).execute()

        check_lead_exist = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{check_value}").execute()["values"]
        if check_lead_exist[0][0] == "1":
            data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{daily_range}").execute()["values"]
        else:
            data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{all_range}").execute()["values"]

        df = pd.DataFrame(data=data[1:], columns=data[0])
        df = df.set_index(df.columns[0])
        return df
    
    def get_tur(self):
        sheet_id = self.sheets_info["tur"]["sheet_id"]
        table_name = self.sheets_info["tur"]["table_name"]
        data_range = self.sheets_info["tur"]["range"]
        which_tur = self.sheets_info["tur"]["which_tur"]
        what_tur = self.sheets_info["tur"]["what_tur"]

        value_input_option = "USER_ENTERED"

        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{which_tur}",
            valueInputOption=value_input_option,
            body={"values": [[what_tur]]}
        ).execute()

        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        df = pd.DataFrame(data=data[1:], columns=data[0])
        df = df.set_index(df.columns[0])
        return df
    
    def get_milliard(self):
        sheet_id = self.sheets_info  ["milliard"]["sheet_id"]
        table_name = self.sheets_info["milliard"]["table_name"]
        data_range = self.sheets_info["milliard"]["range"]

        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        df = pd.DataFrame(data=data[1:], columns=data[0])
        df = df.set_index(df.columns[0])
        return df

    def get_dastur(self):
        sheet_id = self.sheets_info  ["dastur_payment"]["sheet_id"]
        table_name = self.sheets_info["dastur_payment"]["table_name"]
        data_range = self.sheets_info["dastur_payment"]["range"]
        which_tur = self.sheets_info ["dastur_payment"]["which_dastur"]
        what_tur = self.sheets_info  ["dastur_payment"]["what_dastur"]

        value_input_option = "USER_ENTERED"

        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{table_name}!{which_tur}",
            valueInputOption=value_input_option,
            body={"values": [[what_tur]]}
        ).execute()

        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        df = pd.DataFrame(data=data[1:], columns=data[0])
        df = df[["Менежер", "100% тўлов", "Бартер", "5 mln +", "3 mln-4,9 mln", "3 mln -", "Жами Сотув", "Жами сотув сумма", "Тушган сумма", "Қарз Сумма"]]
        df = df.set_index(df.columns[0])
        return df
    
    def _convert_data_to_dict(self, data_array):
        table_dict = {
            # Content
            'header': data_array[0][0],
            'merged_ab': data_array[1][0],
            'c2': data_array[1][2] if len(data_array[1]) > 2 else '',
            'a3': data_array[2][0],
            'b3': data_array[2][1] if len(data_array[2]) > 1 else '',
            'a4': data_array[3][0],
            'b4': data_array[3][1] if len(data_array[3]) > 1 else '',
            'a5': data_array[4][0],
            'b5': data_array[4][1] if len(data_array[4]) > 1 else '',
            'c3_c5': data_array[2][2] if len(data_array[2]) > 2 else '',
        }
        return table_dict

    def get_weekly_sales(self):
        sheet_id = self.sheets_info  ["weekly_sales"]["sheet_id"]
        table_name = self.sheets_info["weekly_sales"]["table_name"]
        data_range = self.sheets_info["weekly_sales"]["range"]

        data = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{table_name}!{data_range}").execute()["values"]
        data.pop(1)
        table1_data = self._convert_data_to_dict(data[:5])
        table2_data = self._convert_data_to_dict(data[6:11])
        return (table1_data, table2_data)
