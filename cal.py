import gsd
import datetime

auth = gsd.Auth()
df = auth.df
time1 = df.iloc[-1, 1]
time2 = df.iloc[-1, 2]
in_time = datetime.datetime.strptime(time1, '%H:%M')
out_time = datetime.datetime.strptime(time2, '%H:%M')
# date_time = datetime.datetime.strptime(dte, '%H:%M')
working_hours = str(out_time - in_time)
print(working_hours)
df['働いた時間'] = working_hours



print(df)