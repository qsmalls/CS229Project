# This is a sample Python script.
import numpy as np
import csv
import pandas as pd
from datetime import *
import random
import time
from meteostat import Point, Hourly
from datetime import datetime

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def update_weather(path):
    data = pd.read_csv(path, low_memory=False)
    data.to_csv('Crash_and_Road_and_Weather_Added_Updated.csv')

def transform_time(date_time):
    # between 1 hour and 12 hours, we have (3600,43200) seconds
    time_diff = random.randint(3600, 43200) * random.choice([-1, 1])
    return date_time + pd.Timedelta(time_diff, unit='S')

def add_30(date_time):
    return date_time + pd.Timedelta(1800, unit='S')

def minus_30(date_time):
    return date_time - pd.Timedelta(1800, unit='S')

def get_weather(input):
    start = datetime.strptime(input.split(',')[0], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(input.split(',')[1], '%Y-%m-%d %H:%M:%S')
    # The point
    point = Point(40.7831, -73.9712)
    # Get hourly data
    fetched_data = Hourly(point, start, end, timezone='America/New_York')
    return fetched_data.fetch().iloc[0]

def data_modification(data):
    # remove index
    data = data.iloc[:, 1:]
    data['timedate'] = data['CRASH DATE'] + ' ' + data['CRASH TIME']
    data['timedate'] = pd.to_datetime(data['timedate'])
    data['timedate'] = data['timedate'].transform(transform_time)

    data['timedate_start'] = data['timedate'].transform(minus_30)
    data['timedate_end'] = data['timedate'].transform(add_30)

    data['timedate'] = data['timedate'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
    data['timedate'] = data['timedate'].astype(str)
    data[['CRASH TIME', 'CRASH DATE']] = data.timedate.str.split(expand=True)

    # Set time period
    data['weather_fetch'] = data['timedate_start'].astype(str) + ',' + data['timedate_end'].astype(str)
    data.to_csv('Crash_and_Road_and_Weather_Added.csv')
    print('weather_fetch column done and written')
    try:
        data.append(data['weather_fetch'].transform(get_weather))
    except Exception as e: print(e)
    data = data.drop(['timedate','timedate_end','timedate_start','weather_fetch'], axis=1)

    data.to_csv('Crash_and_Road_and_Weather_Added.csv')


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M', prop)


def generated_new(data):
    # pick a random time in between 07/01/2012 and 05/31/2022
    list_1 = list()
    for x in range(120613):
        list_1.append(random_date("2012-07-01 00:00", "2022-05-31 23:59", random.random()))
    data['timedate'] = list_1
    data['timedate'] = pd.to_datetime(data['timedate'])
    data['timedate_start'] = data['timedate'].transform(minus_30)
    data['timedate_end'] = data['timedate'].transform(add_30)
    data['weather_fetch'] = data['timedate_start'].astype(str) + ',' + data['timedate_end'].astype(str)

    data['timedate'] = data['timedate'].astype(str)
    data[['CRASH TIME', 'CRASH DATE']] = data.timedate.str.split(expand=True)

    print(data)
    try:
        data.append(data['weather_fetch'].transform(get_weather))
    except Exception as e:
        print(e)
    data = data.drop(['timedate', 'timedate_end', 'timedate_start', 'weather_fetch'], axis=1)
    print('done')
    data.to_csv('All_Roads_Without_Accidents.csv')


def data_cleaning(data):
    # remove index
    data = data.iloc[: , 1:]
    #print(data.count()) to find all 0 columns
    data = data.drop(['FCC','NOMINALDIR','ACCESSIBLE','BOROUGH_IN','STREETWI_1','SPECIAL_DI','FIRE_LANE','TRUCK_ROUT','JOINID','snow','wpgt','tsun'], axis=1)
    #data.to_csv('Crash_and_Road_and_Weather_Cleaned.csv')
    print((data.values == data.values).all(axis=1))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    #df = pd.read_csv('Crash_and_Road_and_Weather.csv', low_memory=False)
    #data_cleaning(df)
    #data_modification(pd.read_csv('Crash_and_Road_and_Weather_Cleaned.csv', low_memory=False))
    generated_new(pd.read_csv('Centerline.csv', low_memory=False))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
