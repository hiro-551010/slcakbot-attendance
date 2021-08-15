from gspread_dataframe import set_with_dataframe
from slackbot.bot import Bot, respond_to
from datetime import datetime, timedelta
import gsd
import re
import pandas as pd

timestamp = datetime.now()
date = timestamp.strftime('%Y/%m/%d')
punch_in_time = timestamp.strftime('%H:%M')
punch_out_time = timestamp.strftime('%H:%M')

def working_hours(wks, cell):
    df = pd.DataFrame(wks.get_all_records())
    time1 = df.iloc[-1, 1]
    time2 = df.iloc[-1, 2]
    in_time = datetime.strptime(time1, '%H:%M')
    out_time = datetime.strptime(time2, '%H:%M')
    # date_time = datetime.datetime.strptime(dte, '%H:%M')
    working_hours = str(out_time - in_time)
    # working_hours記入
    wks.update_cell(cell.row, (cell.col + 1), working_hours)

def punch_out(date, punch_out_time, place_name, username):
    auth = gsd.Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    sheet_name = place_name
    wks = wb.worksheet(title=sheet_name)
    cell = wks.find('0:00')
    working_hours(wks, cell)
    # 退勤時刻記入
    wks.update_cell(cell.row, cell.col, punch_out_time)
    wks2 = wb.worksheet(title=username)
    row = wks.row_values(cell.row)
    row_list = [row]
    df = pd.DataFrame(row_list, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
    set_with_dataframe(wks2, df)

    

punch_out(date, punch_out_time, "こうしえん", "hirokazu551010")