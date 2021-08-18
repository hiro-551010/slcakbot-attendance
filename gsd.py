import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe

class Auth():
    # ワークブックまで開く処理
    SP_CREDENTIAL_FILE = "./secrets/attendance-1.json"
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

def wks_username(date, wks, wks2):
    cell = wks.find(date)
    row = wks.row_values(cell.row)
    list_row = [row]
    df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
    set_with_dataframe(wks2, df2)

def df_append(date, punch_in_time, wks):
    df = pd.DataFrame(wks.get_all_records())
    df = df.append({'日付': date, '出勤時刻': punch_in_time, '退勤時刻': '00:00', '働いた時間': '00:00'}, ignore_index=True)
    set_with_dataframe(wks, df)

def punch_in(date, punch_in_time, place_name, username):
    auth = Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    sheet_name = place_name
    sheet_list = [ws.title for ws in wb.worksheets()]
    if sheet_name in sheet_list:
        wks = wb.worksheet(title=sheet_name)
        cell = wks.find(date)
        if cell:
            row = wks.row_values(cell.row)
            list_row = [row]
            df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
            if username in sheet_list:
                wks2 = wb.worksheet(title=username)
                set_with_dataframe(wks2, df2)
            else:
                wks2 = wb.add_worksheet(title=username, rows=30, cols=100)
                set_with_dataframe(wks2, df2)
        else:
            df_append(date, punch_in_time, wks)
            if username in sheet_list:
                wks2 = wb.worksheet(title=username)
                wks_username(date, wks, wks2)
            else:
                wks2 = wb.add_worksheet(title=username, rows=30, cols=100)
                wks_username(date, wks, wks2)
    else:
        wks = wb.add_worksheet(title=sheet_name, rows="100", cols="30")
        df_append(date, punch_in_time, wks)
        if username in sheet_list:
            wks2 = wb.worksheet(title=username)
            wks_username(date, wks, wks2)
        else:
            wks2 = wb.add_worksheet(title=username, rows="100", cols="30")
            wks_username(date, wks, wks2)

    
def working_hours(wks):
    df = pd.DataFrame(wks.get_all_records())
    time1 = df.iloc[-1, 1]
    time2 = df.iloc[-1, 2]
    in_time = datetime.strptime(time1, '%H:%M')
    out_time = datetime.strptime(time2, '%H:%M')
    working_hour = str(out_time - in_time)
    cell2 = wks.find('0:00')
    wks.update_cell(cell2.row, cell2.col, working_hour)


def punch_out(date, punch_out_time, place_name, username):
    auth = Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    sheet_name = place_name
    wks = wb.worksheet(title=sheet_name)
    cell = wks.find('0:00')
    wks.update_cell(cell.row, cell.col, punch_out_time)
    working_hours(wks)
    wks2 = wb.worksheet(title=username)
    row = wks.row_values(cell.row)
    row_list = [row]
    df = pd.DataFrame(row_list, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
    set_with_dataframe(wks2, df)
