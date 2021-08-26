from datetime import datetime, timedelta

time1 = ''
time2 = ''


def round_working_hours(time1, time2):
    time1 = datetime.strptime(time1, '%H:%M:%S')
    time2 = datetime.strptime(time2, '%H:%M:%S')
    working_hours = time1 - time2
    th = working_hours / timedelta(hours=1)
    th_h = int(th)
    for_round = th - th_h
    if for_round >= 0.75:
        dt_hour = th_h + 1
        print(1, dt_hour, '1時間足されました')
    elif 0.15 <= for_round < 0.75:
        dt_hour = th_h + 0.5
        print(2, dt_hour, '0.5時間足されました')
    else:
        print(4, th_h, '時間は足されませんでした')

round_working_hours(time1, time2)