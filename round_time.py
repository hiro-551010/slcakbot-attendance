from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SP_CREDENTIAL_FILE = "./secrets/attendance.json"
SP_SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
SP_SHEET_KEY = '1AWzy25WkpHFmf83Y15--T-xZdXRFZ2ZALcLEOXGPkvc'
    
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)


wb = gc.open_by_key(SP_SHEET_KEY)
sheet_name = 'hirokazu551010'
wks = wb.worksheet(title=sheet_name)
df = pd.DataFrame(wks.get_all_values())

punch_in = df.iloc[-1, 1]
punch_out = df.iloc[-1, 2]

time1 = punch_out
time2 = punch_in


def round_working_hours(time1, time2):
    time1 = datetime.strptime(time1, '%H:%M')
    time2 = datetime.strptime(time2, '%H:%M')
    working_hours = time1 - time2
    th = working_hours / timedelta(hours=1)
    th_h = int(th)
    for_round = th - th_h
    if for_round >= 0.75:
        dt_hour = th_h + 1
        print(1, dt_hour, '1時間足されました')
        wks.update_cell(2, 4, dt_hour)
    elif 0.15 <= for_round < 0.75:
        dt_hour = th_h + 0.5
        print(2, dt_hour, '0.5時間足されました')
        wks.update_cell(2, 4, dt_hour)
        print(type(dt_hour))
    else:
        print(4, th_h, '時間は足されませんでした')
        print(type(th_h))
        wks.update_cell(2, 4, str(th_h))

round_working_hours(time1, time2)