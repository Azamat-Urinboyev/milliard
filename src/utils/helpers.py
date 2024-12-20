import json
import logging
from datetime import datetime, timedelta

from src.api.calls_fetcher import MoizvonkiApi
from src.api.clockster import Clockster
from src.api.sheets_updater import Sheets
from config.settings import MOIZVONKI_API, MOIZVONKI_USERNAME, CLOCKSTER_TOKEN
from src.api.report_fetcher import Reports
from src.visualization.table_plot import (
     plot_calls,
     plot_productivity,
     plot_productivity2,
     plot_call_time,
     plot_leads,
     plot_weekly_sales,
     plot_tur,
     plot_milliard,
     plot_dastur
)



with open("data/raw/sheets_info.json") as f:
        sheet_info = json.load(f)


def add_yesterdays_calls():
    try:
        moizvonki = MoizvonkiApi(username=MOIZVONKI_USERNAME, api_key=MOIZVONKI_API)
        sheet = Sheets(sheet_id=sheet_info["daily_calls"]["sheet_id"])

        yesterdays_calls = moizvonki.get_yesterdays_calls()
        sheet.update_calls(table_name=sheet_info["daily_calls"]["table_name"], calls=yesterdays_calls)
    except Exception as e:
         logging.error(f"Error adding daily calls:  {e}")


def add_attendance(ndays_before=1):
    try:
        yesterday = datetime.now() - timedelta(days=ndays_before)

        sheet = Sheets(sheet_id=sheet_info["attendance"]["sheet_id"])

        clockster = Clockster(CLOCKSTER_TOKEN)
        attendance = clockster.get_attandance(yesterday)
        sheet.update_attendance(table_name=sheet_info["attendance"]["table_name"], attendance=attendance)
    except Exception as e:
        logging.error(f"Error adding attendance:  {e}")


def get_reports():
    report = Reports()
    results = []

    try:
        calls = report.get_calls()
        calls_dir = plot_calls(calls)
    except Exception as e:
        logging.error(f"Error processing calls: {e}")
        calls_dir = None
    results.append(calls_dir)

    try:
        prod = report.get_productivity()
        prod_dir = plot_productivity(prod)
    except Exception as e:
        logging.error(f"Error processing productivity: {e}")
        prod_dir = None
    results.append(prod_dir)

    try:
        prod = report.get_productivity2()
        prod_dir = plot_productivity2(prod)
    except Exception as e:
        logging.error(f"Error processing productivity2: {e}")
        prod_dir = None
    results.append(prod_dir)

    try:
        call_time = report.get_call_time()
        call_time_dir = plot_call_time(call_time)
    except Exception as e:
        logging.error(f"Error processing call time: {e}")
        call_time_dir = None
    results.append(call_time_dir)

    try:
        lead = report.get_lead_report()
        lead_dir = plot_leads(lead)
    except Exception as e:
        logging.error(f"Error processing leads: {e}")
        lead_dir = None
    results.append(lead_dir)

    try:
        weekly = report.get_weekly_sales()
        weekly_dir = plot_weekly_sales(weekly)
    except Exception as e:
        logging.error(f"Error processing weekly sales: {e}")
        weekly_dir = None
    results.append(weekly_dir)

    try:
        tur = report.get_tur()
        tur_dir = plot_tur(tur)
    except Exception as e:
        logging.error(f"Error processing tur: {e}")
        tur_dir = None
    results.append(tur_dir)

    try:
        milliard = report.get_milliard()
        milliard_tur = plot_milliard(milliard)
    except Exception as e:
        logging.error(f"Error processing milliard: {e}")
        milliard_tur = None
    results.append(milliard_tur)

    try:
        dastur = report.get_dastur()
        dastur_dir = plot_dastur(dastur)
    except Exception as e:
        logging.error(f"Error processing dastur: {e}")
        dastur_dir = None
    results.append(dastur_dir)

    return results