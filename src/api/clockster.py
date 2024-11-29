import requests
import logging
from datetime import datetime
from config.settings import CLOCKSTER_USERS

class Clockster:
    def __init__(self, token) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            'Content-Type': 'application/json',
        }
        self.base_url = "https://api.clockster.com/company/v2"


    def get_attandance(self, date: datetime):
        yesterday_russian_format = date.strftime("%d.%m.%Y")
        yesterday_clockster_format = date.strftime("%Y-%m-%d")

        emp_ids = [ids for name, ids in CLOCKSTER_USERS.items()]
        emp_ids = ",".join(map(str, emp_ids))

        attendance = self._get_attendance_by_ids(date=yesterday_clockster_format, employee_ids=emp_ids)
        if attendance == None:
            return
        attendance = self._format_attendance(attendance)

        sheets_attendance = []
        for user_name, time in attendance.items():
            att = [user_name, yesterday_russian_format, time["clock-in"], time["clock-out"]]
            sheets_attendance.append(att)
            
        return sheets_attendance


    def _get_attendance_by_ids(self, date, employee_ids):
        url = f"{self.base_url}/attendance"
        params = {
            "per_page": 1000,
            "date_start": date,
            "date_end": date,
            "users": employee_ids
        }

        response = requests.get(url=url, params=params, headers=self.headers)
        if response.status_code != 200:
            logging.error("Can't get attendance:  ", response)
            return
        data = response.json()["data"]
        return data
    

    def _format_attendance(self, attendance: list):
        users = {}
        for name, id in CLOCKSTER_USERS.items():
            users[name] = {
                    "clock-in": "_-_",
                    "clock-out": "_-_"
                }
        for user in attendance:
            user_name = f"{user['user']['first_name']} {user['user']['last_name']}".strip()
            time = user["datetime"]
            datetime_obj = datetime.fromisoformat(time)
            time = datetime_obj.strftime("%H:%M")
            if users[user_name]["clock-in"] == "_-_":
                users[user_name] = {
                    "clock-in": time,
                    "clock-out": time
                }
            else:
                if time < users[user_name]["clock-in"]:
                    users[user_name]["clock-in"] = time
                elif time > users[user_name]["clock-out"]:
                    users[user_name]["clock-out"] = time

        return users