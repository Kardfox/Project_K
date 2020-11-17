from project.settings import BASE_DIR
import json
import requests
from datetime import datetime, timedelta
from pytz import UTC

WEEKDAYS = (('Понедельник', 0), ('Вторник', 1), ('Среда', 2), ('Четверг', 3), ('Пятница', 4), ('Суббота', 5), ('Воскресенье', 6))

def get_time(time, interval, sign):
    today = datetime.today()
    time_list = time.split(sign)#['\n', 'Понедельник\n12:00 - 18:00\n', 'Вторник\n14:15 - 16:000\n']
    time_list[len(time_list) - 1] = time_list[len(time_list) - 1] + '\r\n'
    del time_list[0]#['Понедельник\n12:00 - 18:00\n', 'Вторник\n14:15 - 16:000\n']
    time_weekday_list = []
    for t in time_list:
        ti = t.split('\r\n')
        del ti[len(ti) - 1]
        time_weekday_list.append(ti)#[['Понедельник', '12:00 - 18:00'], ['Вторник', '14:15 - 16:15']]
    #Clear time_list and add tidy objects to time_weekday_list
    interval = interval.split(':')#['1', '0']
    free_time = {}
    for i in range(len(time_weekday_list)):
        start_time = {'hour' : time_weekday_list[i][1].split(' - ')[0].split(':')[0], 'minute' : time_weekday_list[i][1].split(' - ')[0].split(':')[1]}
        #Get time of start work day doctor
        end_time = {'hour' : time_weekday_list[i][1].split(' - ')[1].split(':')[0], 'minute' : time_weekday_list[i][1].split(' - ')[1].split(':')[1]}
        #Get time of end work day doctor
        start_datetime = datetime(today.year, today.month, today.day, int(start_time['hour']), int(start_time['minute']))
        end_datetime = datetime(today.year, today.month, today.day, int(end_time['hour']), int(end_time['minute']))
        #Convert string time to datetime
        free_time[time_weekday_list[i][0]] = []
        #Add to free_time name of weekday
        #Multiply start_datetime and end_time on 60(minutes). It returned quantity of minutes and it allows understand which time larger
        while int(start_datetime.hour) * 60 + int(start_datetime.minute) < int(end_datetime.hour) * 60 + int(end_datetime.minute):
            free_time[time_weekday_list[i][0]].append(str(start_datetime.time()))
            #Append start(free) time
            start_datetime += timedelta(hours = int(interval[0]), minutes = int(interval[1]))
            #Addition interval to start_datetime
    return free_time

def style(filename):
    style = open(file = f'{BASE_DIR}/app/static/css/{filename}.css', mode = 'r').read()
    return style

def get_price(name):
    response = requests.get(f"https://api.apteka.ru/Search/ByPhrase?&phrase={name.replace(' ', '+')}&cityId=5e57b422a19759000122967b")
    data = json.loads(response.text)
    try:
        return data['minGroupPrice']
    except TypeError:
        return 'Лекарств не назначено'

def revealing_olds_objs(arr):
    new_objs = []
    for obj in arr:
        if obj.datetime + timedelta(hours = 2) > UTC.localize(datetime.today()) or obj.datetime + timedelta(hours = 2) == UTC.localize(datetime.today()):
            obj.datetime = obj.datetime + timedelta(hours = 2)
            new_objs.append(obj)
        else:
            continue
    return new_objs

def time_to_datetime(time_obj):
    weekday_obj_number = dict(WEEKDAYS)[time_obj[0].split(' ')[0]]
    weekday_new_number = datetime.weekday(datetime.today())
    if weekday_obj_number - weekday_new_number >= 0:
        date = datetime.date(datetime.today() + timedelta(days = weekday_obj_number - weekday_new_number))
        return (date, datetime.time(datetime.strptime(time_obj[0].split(' ')[1], '%H:%M:%S')))
    else:
        return False