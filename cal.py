import gsd
from datetime import datetime
import pandas as pd
from gspread_dataframe import set_with_dataframe
import csv

timestamp = datetime.now()
date = timestamp.strftime('%Y/%m/%d')
punch_in_time = timestamp.strftime('%H:%M')
punch_out_time = timestamp.strftime('%H:%M')

# auth = gsd.Auth()
# wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)

# timestamp = datetime.now()
# today = timestamp.strftime('%Y/%m/%d')
# sheet_name = "こうしえん"
# username = "hirokazu551010"

# wks = wb.worksheet(title=sheet_name)
# df = pd.DataFrame(wks.get_all_records(), )

# todayのセルの番号取得
# cell = wks.find(today)
# row = wks.row_values(cell.row)
# list_row = [row]
# df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
# wks2 = wb.worksheet(title=username)
# set_with_dataframe(wks2, df2)

def punch_in(date, punch_in_time, place_name, username):
    auth = gsd.Auth()
    wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)
    sheet_name = place_name
    sheet_list = [ws.title for ws in wb.worksheets()]
    # place_nameのシート名があった場合
    if sheet_name in sheet_list:
        wks = wb.worksheet(title=sheet_name)
        cell = wks.find(date)
        # ２回目以降は時刻をシートから取得
        # 日付があった場合
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
        # 日付がなかった場合
        else:
            df = pd.DataFrame(wks.get_all_records())
            df = df.append({'日付': date, '出勤時刻': punch_in_time, '退勤時刻': '00:00', '働いた時間': '00:00'}, ignore_index=True)
            # 場所の時刻を打刻
            set_with_dataframe(wks, df)
            # １回目の人の時刻を打刻
            if username in sheet_list:
                wks2 = wb.worksheet(title=username)
                cell = wks.find(date)
                row = wks.row_values(cell.row)
                list_row = [row]
                df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
                set_with_dataframe(wks2, df2)
            else:
                wks2 = wb.add_worksheet(title=username, rows=30, cols=100)
                cell = wks.find(date)
                row = wks.row_values(cell.row)
                list_row = [row]
                df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
                set_with_dataframe(wks2, df2)
    
    # place_nameのシート名がなかった場合
    else:
        wks = wb.add_worksheet(title=sheet_name, rows="100", cols="30")
        df = pd.DataFrame(wks.get_all_records())
        df = df.append({'日付': date, '出勤時刻': punch_in_time, '退勤時刻': '00:00', '働いた時間': '00:00'}, ignore_index=True)
        set_with_dataframe(wks, df)
        if username in sheet_list:
            wks2 = wb.worksheet(title=username)
            cell = wks.find(date)
            row = wks.row_values(cell.row)
            list_row = [row]
            df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
            set_with_dataframe(wks2, df2)
        else:
            wks2 = wb.add_worksheet(title=username, rows=30, cols=100)
            cell = wks.find(date)
            row = wks.row_values(cell.row)
            list_row = [row]
            df2 = pd.DataFrame(list_row, columns=["日付", "出勤時刻", "退勤時刻", "働いた時間"])
            set_with_dataframe(wks2, df2)

punch_in(date, punch_in_time, "こうしえん", "hirokazu551010")






# for date in df.iloc[:,0]:
#     print(df[date] == today)
    # if date == today:
    #     df.find(today)
    #     wks2 = wb.worksheet(title=username)






