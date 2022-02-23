from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import set_with_dataframe

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


def wks_username(wks):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y/%m/%d')
    # if date:
    #     cell = wks.find(date)
    #     row = wks.row_values(cell.row)
    # else:
    #     wks.update_cell(-1, 1, date)

    try:
        cell = wks.find(date)
        row = wks.row_values(cell.row)
    except:
        col_list = wks.col_values(1)
        row_number = len(col_list) + 1
        wks.update_cell(row_number, 1, date)
    


wks_username(wks)