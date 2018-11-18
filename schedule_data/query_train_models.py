# query_train_models.py
# Query train models data
# - Query the vehicle models of the train, and modify the train icons in the schedule data files.
# - 查询列车车型，并修改列车时刻文件中的车型图标。
# - author: ZHZHH


import numpy as np
import pandas as pd
import json
import sys
import datetime
import time
import re
from urllib import request, parse
from urllib.error import URLError, HTTPError


# search train model by train name
def get_train_model(train_name, models, patterns):
    if not train_name[0] in ['G', 'D', 'C', 'S']:
        return 'Unknown'
    for key, codes in models.items():
        for code in codes:
            if code == train_name:
                return key;
    for key, pattern in patterns.items():
        if re.match(pattern, train_name):
            return key;
    return 'Unknown'


# icon file names of each train model
icon_names = {'Unknown': 'unknown', 
'CRH1A-A型': 'crh1a-a',      'CRH1A-A型重联': 'crh1a-a',
'新CRH1B型': 'crh1b-new',
'CRH1E型':   'crh1e', 
'新CRH1E型': 'crh1e-new',
'CRH2A型': 'crh2a',          'CRH2A型重联': 'crh2a', 
'CRH2A统型': 'crh2a-t',      'CRH2A统型重联': 'crh2a-t',
'CRH2B型': 'crh2b',                 
'CRH2C型': 'crh2c1',         'CRH2C型重联': 'crh2c1', 
'CRH3C型': 'crh3c',          'CRH3C型重联': 'crh3c', 
'CRH380A型': 'crh380a',      'CRH380A型重联': 'crh380a',
'CRH380A统型': 'crh380a',    'CRH380A统型重联': 'crh380a',
'CRH380AL型': 'crh380a',     '新CRH380AL型': 'crh380a',
'CRH380B型': 'crh380b',      'CRH380B型重联': 'crh380b',
'CRH380B统型': 'crh380b',    'CRH380B统型重联': 'crh380b',
'CRH380BL型': 'crh380b',     '新CRH380BL型': 'crh380b',
'CRH380CL型': 'crh380c',  
'CRH380D型': 'crh380d',      'CRH380D型重联': 'crh380d',
'CRH380D统型': 'crh380d',    'CRH380D统型重联': 'crh380d',
'CR400AF型': 'cr400af',      'CR400AF型重联': 'cr400af',
'CR400AF-A型': 'cr400af',
'CR400BF型': 'cr400bf',      'CR400BF型重联': 'cr400bf',
'CR400BF-A型': 'cr400bf'}

# query train model data from moerail.ml
print('Downloading train models data...')
url_model = r'https://moerail.ml/models.json'
req = request.Request(url=url_model)
try:
    model_res = request.urlopen(req)
except (HTTPError, URLError):
    print('Failed to get train model information from moerail.ml!')
    sys.exit()
else:
    model_str = model_res.read()
# decode JSON to Object (JSON转为对象)
try:
    models = json.loads(model_str)
except json.JSONDecodeError:
    print('Failed to decode train model information from moerail.ml!')
    sys.exit()
patterns = models[':']
models.pop(':')

# while 1:
#     print(get_train_model(input(">> "), models, patterns))

# modify the train icons in the schedule data files
print('Modifying train icons...')
fo = open("schedule_data_edited_down_1110-02.csv",'r',encoding='utf_8_sig')
fw = open("temp.csv",'w',encoding='utf_8_sig')
model_counts = {'Unknown': 0}
line = fo.readline() 
while line:
    if line.startswith("TRAIN"):
        if "icon" in line:
            result = re.search(r'TRAIN,(.*?),', line)
            if not result is None:
                train_name = result.group(1)
                icon_name = get_train_model(train_name, models, patterns)
                
                if icon_name in model_counts:
                    model_counts[icon_name] += 1
                else:
                    model_counts[icon_name] = 1
                    
                if icon_name in icon_names:
                    icon_name = icon_names[icon_name]
                line = re.sub(r'icon', icon_name, line)
    
    fw.write(line)
    line = fo.readline()

print(model_counts)
print('Done.')
fo.close()
fw.close()