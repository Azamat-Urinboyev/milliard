from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.types.input_file import FSInputFile
import logging
import pytz

from src.utils.helpers import add_yesterdays_calls, add_attendance, get_reports
from config.settings import GROUP_ID



class SchedulerManager:
    def __init__(self, bot):
        self.scheduler = AsyncIOScheduler(timezone=pytz.UTC)
        self.bot = bot

    async def _sending_reports(self):
        report_files = get_reports()
        for file in report_files:
            try:
                photo = FSInputFile(file)
                await self.bot.send_photo(chat_id=GROUP_ID, photo=photo)
            except Exception as e:
                logging.error(f"Error sending pictures: {e}")


    def start(self):
        #updating calls
        calls_update_trigger = CronTrigger(hour=8, minute=5)
        self.scheduler.add_job(func=add_yesterdays_calls, trigger=calls_update_trigger)

        #update attendance
        attendance_trigger = CronTrigger(hour=8, minute=5)
        self.scheduler.add_job(func=add_attendance, trigger=attendance_trigger)

        #sending reports
        report_trigger = CronTrigger(hour=10, minute=00, day_of_week="tue-sun")
        self.scheduler.add_job(func=self._sending_reports, trigger=report_trigger)


        self.scheduler.start()