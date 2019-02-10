# query_schedule_12306.py
# Query train schedule data
# - Query train schedule data from 12306.cn for Train Animation Generator
# - 从12306网站查询列车时刻数据，用于生成列车运行略图
# - author: ZHZHH

# - updates:
# -- 2018-11-01: 实现站间列车信息查询、列车停站信息查询，实现数据CSV存储，进行测试和参数调整。
# -- 2018-11-03: 实现文本交互式数据查询。


import numpy as np
import pandas as pd
import json
import sys
import datetime
import time
import configparser
from urllib import request, parse
from urllib.error import URLError, HTTPError


# text-based user interface (文本交互式数据查询)
def main():

    print("\nTRAIN SCHEDULE DATA for Train Animation Generator")
    print("- Query train schedule data from 12306.cn\n")
    
    date = input("Please input the date of the schedule (YYYY-mm-dd): ")
    icon_id = input("Please input the default icon id: ")
    
    cmd = ''
    while cmd != '0':
        print("\n- Command Codes:")
        print("-- [1] Add trains by train names.")
        print("-- [2] Add trains by two station code.")
        print("-- [8] Preset command 1 (Shanghai -> Hangzhou)")
        print("-- [9] Preset command 2 (Hangzhou -> Shanghai)")
        print("-- [0] EXIT")
        cmd = input("Please input a command code: ")
        
        if cmd == '1':
            print("Add trains by train names.")
            track_id = input("Default track id (1/2): ")
            direction = input("Default direction (U/D): ")
            train_name = ''
            csv_df = pd.DataFrame(columns=['type', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])
            while train_name.lower() != 'save':
                train_name = input("Please input a train name (input 'show' to show all data; input 'save' to save data): ")
                if train_name.lower() == 'show':
                    print(csv_df)
                elif train_name.lower() == 'save':
                    break;
                elif train_name == '':
                    print('')
                else:
                    csv_df = csv_df.append(query_single_train(train_name, date, [icon_id, track_id, direction]), True)
                    print('Done.')
            if csv_df is None:
                print('Data is empty! No data to save.')
            else:
                result = 1
                while result != 0:
                    filename = input("File name (*.csv, input 'delete' to discard data): ")
                    if filename == 'delete':
                        break
                    if filename != '':
                        if not csv_df is None:
                            result = save(csv_df, filename)
                        else:
                            result = 0
                            
        elif cmd == '2':
            print("Add trains by two station code.")
            from_station = input("From (Station code): ")
            from_strict = input("Exclude other station in the same city? (y/[n]): ") == 'y'
            to_station = input("To (Station code): ")
            to_strict = input("Exclude other station in the same city? (y/[n]): ") == 'y'
            train_class = list(input("Train class filter: "))
            if len(train_class) == 0:
                train_class = None
            track_id = input("Default track id (1/2): ")
            direction = input("Default direction (U/D): ")            
            csv_df = query_trains_between(from_station, to_station, train_class, date, from_strict, to_strict, [icon_id, track_id, direction])
            if csv_df is None:
                print('Data is empty! No data to save.')
            else:
                result = 1
                while result != 0:
                    filename = input("File name (*.csv, input 'delete' to discard data): ")
                    if filename == 'delete':
                        break
                    if filename != '':
                        if not csv_df is None:
                            result = save(csv_df, filename)
                        else:
                            result = 0
            
        elif cmd == '8':
            print("Preset command 1 (Shanghai -> Hangzhou)")
            csv_df = query_trains_between('AOH', 'HGH', ['G', 'D', 'C'], date, True, False, [icon_id, '2', 'D'])
            save(csv_df, 'schedule_data_raw_down.csv')
            
        elif cmd == '9':
            print("Preset command 2 (Hangzhou -> Shanghai)")
            csv_df = query_trains_between('HGH', 'AOH', ['G', 'D', 'C'], date, False, True, [icon_id, '1', 'U'])
            save(csv_df, 'schedule_data_raw_up.csv')
            
        elif cmd == '0':
            print("")
            break;
        elif cmd == '':
            print("")
            # do nothing
        else:
            print("Invalid command code!")


# query the information of a train by train name (根据车次查询单个列车信息)
def query_single_train(train_name='G1', date=None, default_params=None):

    # search train No. by train name (根据车次查车次编号)
    # query JSON data from 12306 (下载JSON数据)
    url_train = r'https://search.12306.cn/search/v1/train/search'  # the url may be changed, check the latest on 12306.cn
    parameter_dict = {'keyword': train_name,
                      'date': (datetime.date.today() + datetime.timedelta(days=1)).strftime(
        '%Y%m%d') if date is None else date.replace('-', '')}
    req = request.Request(url='%s%s%s' % (url_train, '?', parse.urlencode(parameter_dict)))
    try:
        train_res = request.urlopen(req)
    except (HTTPError, URLError):
        print('Failed to get train code from 12306!')
        return None
    else:
        train_str = train_res.read()
    # decode JSON to Object (JSON转为对象)
    try:
        train_json = json.loads(train_str)
    except json.JSONDecodeError:
        print('Failed to decode train information from 12306!')
        # print(train_str.decode('utf-8'))
        return None
    # validate train name (验证查到的车次)
    train_no = None
    if isinstance(train_json, dict):
        if 'data' in train_json:
            if isinstance(train_json['data'], list):
                for train_data in train_json['data']:
                    if isinstance(train_data, dict):
                        if ('station_train_code' in train_data) and ('train_no' in train_data):
                            if train_data['station_train_code'] == train_name:
                                train_no = train_data['train_no']
                                break
    if train_no is None:
        print('Train {0} not found!'.format(train_name))
        # print(train_json)
        return None
    
    # train info (整理列车信息)
    train = {'train_no': train_no, 'train_name': train_name, 'from': 'XXX', 'to': 'XXX', 'destination': 'XXX'}
    train['train_class'] = train_name[0] if train_name[0].isalpha() else '0'

    # set other params (设置其他参数)
    if default_params is None:
        default_params = ['1', '1', 'D']
    train['icon_id'] = default_params[0]
    train['class_color'] = train['train_class']
    train['destination_color'] = 'TO_OTHER_LINES'

    # query stop information (查询停站时刻信息)
    print('Querying stops info...')
    csv_df = query_stops_of(train, date, default_params[1], default_params[2], 1)
    
    return csv_df


# query the information of trains between two stations (查询站间列车信息)
def query_trains_between(from_station_code='BJP', to_station_code='SHH', train_class=None, date=None,
                         strict_from_station=False, strict_to_station=False, default_params=None):

    # exclude same station (排除同站)
    if from_station_code == to_station_code:
        print('Same station!')
        return
    print('Querying trains info...')

    # search trains information by two station code (根据两站编号查两站间车次信息)
    # query JSON data from 12306 (下载JSON数据)
    url_train = r'https://kyfw.12306.cn/otn/leftTicket/queryZ'  # the url may be changed, check the latest on 12306.cn
    parameter_dict = {'leftTicketDTO.train_date': (datetime.date.today() + datetime.timedelta(days=1)).strftime(
        '%Y-%m-%d') if date is None else date,
                      'leftTicketDTO.from_station': from_station_code,
                      'leftTicketDTO.to_station': to_station_code,
                      'purpose_codes': 'ADULT'}
    req = request.Request(url='%s%s%s' % (url_train, '?', parse.urlencode(parameter_dict)))
    try:
        train_res = request.urlopen(req)
    except (HTTPError, URLError):
        print('Failed to get train information from 12306!')
        return None
    else:
        train_str = train_res.read()
    # decode JSON to Object (JSON转为对象)
    try:
        train_json = json.loads(train_str)
    except json.JSONDecodeError:
        print('Failed to decode train information from 12306!')
        # print(train_str.decode('utf-8'))
        return None
    # print(train_json['data']['result'])
    train_list = None
    if isinstance(train_json, dict):
        if 'data' in train_json:
            if isinstance(train_json['data'], dict):
                if 'result' in train_json['data']:
                    if isinstance(train_json['data']['result'], list):
                        train_list = train_json['data']['result']
    if train_list is None:
        print('Unexpected data structure from 12306!')
        return None
    # transfer data object to DataFrame (整理数据为DataFrame: 列车编号, 车次, 出发站, 到达站, 终到站)
    train_df = pd.DataFrame(columns=['train_no', 'train_name', 'from', 'to', 'destination'])
    for row in train_list:
        row_list = str(row).split('|', maxsplit=11)
        train_df.loc[train_df.shape[0]] = {'train_no': row_list[2], 'train_name': row_list[3], 'from': row_list[6],
                                           'to': row_list[7], 'destination': row_list[5]}
    # print(train_df)

    # filter from_station and to_station strictly (筛选精确车站)
    if strict_from_station:
        train_df = train_df[train_df['from'] == from_station_code]
    if strict_to_station:
        train_df = train_df[train_df['to'] == to_station_code]

    # filter train class (筛选列车种别)
    train_df['train_class'] = list(map(lambda tn: tn[0] if tn[0].isalpha() else '0', train_df['train_name']))
    if isinstance(train_class, list):
        train_df = train_df[train_df['train_class'].isin(train_class)]

    # set other params (设置其他参数)
    if default_params is None:
        default_params = ['1', '1', 'D']
    train_df['icon_id'] = default_params[0]
    train_df['class_color'] = train_df['train_class']
    train_df['destination_color'] = 'TO_OTHER_LINES'
    for index in train_df.index:
        if train_df['destination'].loc[index] == to_station_code:
            train_df['destination_color'].loc[index] = 'TO_MAIN_TERMINAL'
        elif train_df['destination'].loc[index] == train_df['to'].loc[index]:
            train_df['destination_color'].loc[index] = 'TO_SUB_TERMINAL'
    # print(train_df)

    # query stop information (查询停站时刻信息)
    print('{0} train(s) found.'.format(len(train_df)))
    print('Querying stops info...')
    csv_df = pd.DataFrame(columns=['type', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])
    for index in train_df.index:
        csv_df = csv_df.append(
            query_stops_of(train_df.loc[index], date, default_params[1], default_params[2], len(train_df)), True)
    print()
    
    return csv_df


# query the information of the stops of a train (查询列车停站时刻信息)
def query_stops_of(train, date=None, default_track='1', default_direction='D', train_count=100, processed=[]):
    
    # progress bar (进度条)
    if len(processed) == 0:
        processed.append(0)  # begin to record the count of trains processed (开始记录函数运行次数)
        processed.append(train_count)
    if processed[0] >= processed[1] or processed[1] != train_count:  # if processed number is great than total number, start a new progress bar
        processed[0] = 0
        processed[1] = train_count
    sys.stdout.write("{0}".format(progress_bar(processed[0] / train_count, 48)))
    sys.stdout.flush()

    # searche train stops station and schedule by train No. (根据列车编号查询列车停站时刻)
    # query JSON data from 12306 (下载JSON数据)
    url_train = r'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'  # the url may be changed, check the latest on 12306.cn
    parameter_dict = {'train_no': train['train_no'],
                      'from_station_telecode': train['from'],
                      'to_station_telecode': train['to'],
                      'depart_date': (datetime.date.today() + datetime.timedelta(days=1)).strftime(
                          '%Y-%m-%d') if date is None else date}
    req = request.Request(url='%s%s%s' % (url_train, '?', parse.urlencode(parameter_dict)))
    try:
        stop_res = request.urlopen(req)
    except (HTTPError, URLError):
        print('\nFailed to get train stops information of {0} from 12306!'.format(train['train_name']))
        return None
    else:
        stop_str = stop_res.read()
    # decode JSON to Object (JSON转为对象)
    try:
        stop_json = json.loads(stop_str)
    except json.JSONDecodeError:
        print('\nFailed to decode train stops information of {0} from 12306!'.format(train['train_name']))
        # print(stop_str.decode('utf-8'))
        return None
    # print(stop_json['data']['result'])
    stop_list = None
    if isinstance(stop_json, dict):
        if 'data' in stop_json:
            if isinstance(stop_json['data'], dict):
                if 'data' in stop_json['data']:
                    if isinstance(stop_json['data']['data'], list):
                        stop_list = stop_json['data']['data']
    if stop_list is None:
        print('\nUnexpected data structure of {0} from 12306!'.format(train['train_name']))
        return None
    
    # transfer data object to DataFrame (整理数据为DataFrame)
    stop_df = pd.DataFrame(columns=['type', 'arr_time', 'dep_time', 'station_id',
                                    'track_id', 'in_direction', 'out_direction'])
    index = 0
    for stop in stop_list:
        if isinstance(stop, dict):
            stop_type = 'STOP'

            # initial station
            if index == 0:  # arrived at initial station 15 minutes before departure
                arr_time = str2time(stop['start_time']) - datetime.timedelta(minutes=15)
                stop_type = 'INITIAL'
            else:
                arr_time = str2time(stop['arrive_time'])

            # terminal station
            if index == len(stop_list) - 1:  # leave from terminal station 15 minutes after arrival
                dep_time = str2time(stop['arrive_time']) + datetime.timedelta(minutes=15)
                stop_type = 'TERMINAL'
                train["destination"] = stop['station_name']
            else:
                dep_time = str2time(stop['start_time'])

            stop_df.loc[stop_df.shape[0]] = {'type': stop_type, 'arr_time': time2str(arr_time),
                                             'dep_time': time2str(dep_time), 'station_id': stop['station_name'],
                                             'track_id': default_track, 'in_direction': default_direction,
                                             'out_direction': default_direction}

            # ======== OPTIONAL CODE - BEGIN ======== #
            # Add additional way points for Shanghai-Hangzhou Hi-speed Line
            # Comment or modify the following OPTIONAL CODE for other lines
            # (沪杭客运专线专用代码，自动添加上海虹桥、杭州、杭州东前后的定位点)
            current_station_id = stop_df.shape[0] - 1
            if stop['station_name'] == "上海虹桥":
                if default_direction == 'U':
                    pass_time = arr_time - datetime.timedelta(minutes=7)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J4',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != len(stop_list) - 1:
                        pass_time = dep_time + datetime.timedelta(minutes=5)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E3',
                                                         'track_id': default_track, 'in_direction': default_direction,
                                                         'out_direction': default_direction}
                elif default_direction == 'D':
                    pass_time = dep_time + datetime.timedelta(minutes=7)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J4',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != 0:
                        pass_time = arr_time - datetime.timedelta(minutes=5)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E3',
                                                         'track_id': default_track, 'in_direction': default_direction,
                                                         'out_direction': default_direction}

            if stop['station_name'] == "杭州东":
                if default_direction == 'U':
                    pass_time = dep_time + datetime.timedelta(minutes=5)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J3',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != 0:
                        pass_time = arr_time - datetime.timedelta(minutes=6)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E2',
                                                         'track_id': default_track, 'in_direction': default_direction,
                                                         'out_direction': default_direction}
                elif default_direction == 'D':
                    pass_time = arr_time - datetime.timedelta(minutes=5)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J3',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != len(stop_list) - 1:
                        pass_time = dep_time + datetime.timedelta(minutes=6)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E2',
                                                         'track_id': default_track, 'in_direction': default_direction,
                                                         'out_direction': default_direction}

            if stop['station_name'] == "杭州":
                if default_direction == 'U':
                    pass_time = dep_time + datetime.timedelta(minutes=7)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J2',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    pass_time = dep_time + datetime.timedelta(minutes=12)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J3',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != 0:
                        stop_df.loc[current_station_id]['in_direction'] = 'D'
                        pass_time = arr_time - datetime.timedelta(minutes=12)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'J1',
                                                         'track_id': default_track, 'in_direction': 'D',
                                                         'out_direction': 'D'}
                        pass_time = arr_time - datetime.timedelta(minutes=14)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E1',
                                                         'track_id': default_track, 'in_direction': 'D',
                                                         'out_direction': 'D'}
                elif default_direction == 'D':
                    pass_time = arr_time - datetime.timedelta(minutes=7)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J2',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    pass_time = arr_time - datetime.timedelta(minutes=12)
                    stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                     'dep_time': time2str(pass_time), 'station_id': 'J3',
                                                     'track_id': default_track, 'in_direction': default_direction,
                                                     'out_direction': default_direction}
                    if index != len(stop_list) - 1:
                        stop_df.loc[current_station_id]['out_direction'] = 'U'
                        pass_time = dep_time + datetime.timedelta(minutes=12)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'J1',
                                                         'track_id': default_track, 'in_direction': 'U',
                                                         'out_direction': 'U'}
                        pass_time = dep_time + datetime.timedelta(minutes=14)
                        stop_df.loc[stop_df.shape[0]] = {'type': 'PASS', 'arr_time': time2str(pass_time),
                                                         'dep_time': time2str(pass_time), 'station_id': 'E1',
                                                         'track_id': default_track, 'in_direction': 'U',
                                                         'out_direction': 'U'}
            # ======== OPTIONAL CODE - END   ======== #
        index += 1

    # transfer to DataFrame for CSV (转为用于保存CSV的DataFrame)
    csv_train_df = pd.DataFrame(columns=['type', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])
    csv_train_df.loc[0] = {'type': 'TRAIN', 'p1': train['train_name'], 'p2': train['destination'],
                           'p3': train['icon_id'], 'p4': train['class_color'], 'p5': train['destination_color'],
                           'p6': ''}
    csv_stop_df = pd.DataFrame(columns=['type', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])
    csv_stop_df['type'] = stop_df["type"]
    csv_stop_df['p1'] = stop_df["arr_time"]
    csv_stop_df['p2'] = stop_df["dep_time"]
    csv_stop_df['p3'] = stop_df["station_id"]
    csv_stop_df['p4'] = stop_df["track_id"]
    csv_stop_df['p5'] = stop_df["in_direction"]
    csv_stop_df['p6'] = stop_df["out_direction"]
    csv_train_df = csv_train_df.append(csv_stop_df, True)

    # progress bar +1 (进度条 +1)
    processed[0] += 1  # record the count of trains processed
    sys.stdout.write('\b' * 48)
    return csv_train_df


# save data frame as CSV
def save(df, filename):
    print('Saving...')
    try:
        df.to_csv(filename, index=False, header=False, encoding='utf_8_sig')
    except IOError:
        print('Failed to save schedule data!')
        return 1
    else:
        print('Done.')
        return 0


# transfer string to time
def str2time(time_string):
    t = time.strptime(time_string, '%H:%M')
    return datetime.datetime(year=2000, month=1, day=1, hour=t.tm_hour, minute=t.tm_min)


# transfer time to string, use 3 ~ 26 hour one day
def time2str(t):
    hour = t.hour + 24 if t.hour <= 2 else t.hour
    return "{0}:{1:02d}".format(hour, t.minute)


# show progress bar
def progress_bar(percentage, str_width):
    head = '|'
    tail = '|[{0:3d}%]'.format(int(percentage * 100))
    filled_block = '█'
    remain_block = '　▏▎▍▌▋▊▉'
    block_count = int((str_width - len(head) - len(tail)) / 2)
    filled_block_count_x8 = percentage * block_count * 8
    filled_block_count = int(filled_block_count_x8 / 8)
    remain_block_id = int(filled_block_count_x8 % 8)
    return head + (filled_block * filled_block_count +
                   remain_block[remain_block_id]).ljust(block_count, '　')[0:block_count] + tail


if __name__ == '__main__':
    main()
