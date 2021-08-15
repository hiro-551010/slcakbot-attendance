import gsd
from datetime import datetime
import pandas as pd
from gspread_dataframe import set_with_dataframe
import csv

timestamp = datetime.now()
date = timestamp.strftime('%Y/%m/%d')
punch_in_time = timestamp.strftime('%H:%M')
punch_out_time = timestamp.strftime('%H:%M')

auth = gsd.Auth()
wb = auth.gc.open_by_key(auth.SP_SHEET_KEY)

timestamp = datetime.now()
today = timestamp.strftime('%Y/%m/%d')
sheet_name = "こうしえん"
username = "hirokazu551010"

wks = wb.worksheet(title=sheet_name)
df = pd.DataFrame(wks.get_all_records())

time1 = df.iloc[-1, 1]
time2 = df.iloc[-1, 2]
in_time = datetime.strptime(time1, '%H:%M')
out_time = datetime.strptime(time2, '%H:%M')


# def working_hours(wks):
#     df = pd.DataFrame(wks.get_all_records())
#     time1 = df.iloc[-1, 1]
#     time2 = df.iloc[-1, 2]
#     in_time = datetime.strptime(time1, '%H:%M')
#     out_time = datetime.strptime(time2, '%H:%M')
#     working_hours = str(out_time - in_time)
#     wks.update_cell(2, (3 + 1), working_hours)
#     print(working_hours)

# working_hours(wks)








