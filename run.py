from slackbot.bot import Bot, respond_to
from datetime import datetime, timedelta
import gsd
import re

bot = Bot()

# @respond_to('^出勤$')
# def bot1(message):
#     sheet_name = message.user['real_name']
#     message.send(f'出勤時刻は、{punch_in_time}です')

# @respond_to('^退勤$')
# def bot2(message):
#     sheet_name = message.user['name']
#     message.send(f'退勤時刻は、{punch_out_time}です')
#     gsd.punch_out(date, punch_out_time, sheet_name)

@respond_to('^出勤\s+\S.*')
def bot3(message):
    place_name = message.body['text'][3:]
    username = message.user['real_name']
    timestamp = datetime.now() + timedelta(hours=9)
    date = timestamp.strftime('%Y/%m/%d')
    punch_in_time = timestamp.strftime('%H:%M')
    message.send(f'{place_name}の出勤時刻は{punch_in_time}です')
    gsd.punch_in(date, punch_in_time, place_name, username)

@respond_to('^退勤\s+\S.*')
def bot4(message):
    place_name = message.body['text'][3:]
    username = message.user['name']
    timestamp = datetime.now() + timedelta(hours=9)
    date = timestamp.strftime('%Y/%m/%d')
    punch_out_time = timestamp.strftime('%H:%M')
    message.send(f'{place_name}の退勤時刻は{punch_out_time}です')
    gsd.punch_out(date, punch_out_time, place_name, username)
    
bot.run()