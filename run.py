from slackbot.bot import Bot, respond_to
from datetime import datetime, timedelta
import gsd

timestamp = datetime.now() + timedelta(hours=9)
date = timestamp.strftime('%Y/%m/%d')
punch_in_time = timestamp.strftime('%H:%M')
punch_out_time = timestamp.strftime('%H:%M')

bot = Bot()

@respond_to('出勤')
def bot1(message):
    sheet_name = message.user['real_name']
    message.send(f'出勤時刻は、{punch_in_time}です')
    gsd.punch_in(date, punch_in_time, sheet_name)

@respond_to('退勤')
def bot2(message):
    sheet_name = message.user['name']
    message.send(f'退勤時刻は、{punch_out_time}です')
    gsd.punch_out(date, punch_out_time, sheet_name)
    
bot.run()