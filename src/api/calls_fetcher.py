import time
import logging
import pytz
import requests
from config.settings import MOIZVONKI_MANAGER_MAP, MOIZVONKI_DIRECTION, MOIZVONKI_ANSWERED
from datetime import datetime, timedelta, timezone



class MoizvonkiApi:
    def __init__(self, username, api_key, max_retries=10) -> None:
        self.max_retries = max_retries
        self.base_url = "https://salesdoctoruz.moizvonki.ru/api/v1"
        self.payload = {
            "user_name": username,
            "api_key":api_key,
            "action": "calls.list",
            "supervised": 1
        }

    def _request_calls(self, payload):
        response = requests.post(self.base_url, json=payload)
        if response.status_code != 200:
            logging.error(f"{response}")
        
        return response.json()
    
    def _convert_unix_2_normal_fulldate(self, unix_time):
        utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)
        local_timezone = pytz.timezone("Asia/Tashkent")
        local_time = utc_time.astimezone(local_timezone)
        formatted_datetime = local_time.strftime("%d-%m-%Y %H:%M:%S")
        return formatted_datetime

    def _seconds_to_hms(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

    def _retrive_data(self, calls: list):
        data = []
        for call in calls:
            direction = MOIZVONKI_DIRECTION[call["direction"]]
            manager = MOIZVONKI_MANAGER_MAP[call["user_id"]]
            phone_num = call["client_number"]
            date = self._convert_unix_2_normal_fulldate(call["start_time"])
            duration = call["duration"]
            duration_formatted = self._seconds_to_hms(duration)
            answered = MOIZVONKI_ANSWERED[call["answered"]]

            data.append([date, manager, phone_num, "", direction, answered, duration_formatted, "", ""])

        return data


    def get_yesterdays_calls(self):
        yesterday = datetime.today() - timedelta(days=1)
        yesterday = yesterday.replace(hour=0, minute=0, second=0)
        yesterday = int(time.mktime(yesterday.timetuple()))
        today = datetime.today()
        today = today.replace(hour=0, minute=0, second=0)
        today = int(time.mktime(today.timetuple()))

        payload = self.payload
        payload["from_date"] = yesterday
        payload["to_date"] = today
        payload["from_offset"] = 0

        calls = []
        remainings = None
        attempt = 0
        while remainings != 0:
            try:
                result = self._request_calls(payload)
                next_offset = result["results_next_offset"]
                remainings= result["results_remains"]
                calls += self._retrive_data(result["results"])
                payload["from_offset"] = next_offset
            except Exception as e:
                attempt += 1
                wait_time = 2**(attempt)
                logging.warning(f"Rate limited. Waiting {wait_time} seconds.")
                logging.error(f"Error occured: {e}")
                time.sleep(wait_time)
                
        return calls
