import pandas as pd
from slackbot.bot import Bot, respond_to
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe


class Auth():
    # ワークブックまで開く処理
    SP_CREDENTIAL_FILE = "./secrets/attendance.json"
    SP_SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    SP_SHEET_KEY = '1AWzy25WkpHFmf83Y15--T-xZdXRFZ2ZALcLEOXGPkvc'

    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.SP_CREDENTIAL_FILE, self.SP_SCOPE)
        self.gc = gspread.authorize(credentials)
        # self.wb = gc.open_by_key(self.SP_SHEET_KEY)
        # self.sheet_name = sheet_name
        # self.wks = self.wb.worksheet(sheet_name)
        # self.df = pd.DataFrame(self.wks.get_all_records())

def punch_in(date, punch_in_time, sheet_name):
    auth = Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    sheet_list = [ws.title for ws in wb.worksheets()]
    if sheet_name in sheet_list:
        wks = wb.worksheet(title=sheet_name)
        df = pd.DataFrame(wks.get_all_records())
        df = df.append({'日付': date, '出勤時刻': punch_in_time, '退勤時刻': '00:00', '働いた時間': '00:00'}, ignore_index=True)
        set_with_dataframe(wks, df)
    else:
        wks = wb.add_worksheet(title=sheet_name, rows="100", cols="30")
        df = pd.DataFrame(wks.get_all_records())
        df = df.append({'日付': date, '出勤時刻': punch_in_time, '退勤時刻': '00:00', '働いた時間': '00:00'}, ignore_index=True)
        set_with_dataframe(wks, df)

    
def punch_out(date, punch_out_time, sheet_name):
    auth = Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    wks = wb.worksheet(title=sheet_name)
    cell = wks.find('0:00')
    # 退勤時刻記入
    wks.update_cell(cell.row, cell.col, punch_out_time)

    # working_hours算出
    df = pd.DataFrame(wks.get_all_records())
    time1 = df.iloc[-1, 1]
    time2 = df.iloc[-1, 2]
    in_time = datetime.datetime.strptime(time1, '%H:%M')
    out_time = datetime.datetime.strptime(time2, '%H:%M')
    # date_time = datetime.datetime.strptime(dte, '%H:%M')
    working_hours = str(out_time - in_time)
    # working_hours記入
    wks.update_cell(cell.row, (cell.col + 1), working_hours)

