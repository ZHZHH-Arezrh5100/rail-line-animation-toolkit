# for 1107 to 1108
# this script is not well tested.

import re

fo = open("schedule_data_edited_up_1107.csv",'r',encoding='utf_8_sig')
fw = open("schedule_data_edited_up_1108.csv",'w',encoding='utf_8_sig')
read_next = True
count = 0
line = fo.readline() 
while line:
    read_next = True
    if line.startswith("TRAIN"):
        searchObj = re.search(r'\(([0-9])\)', line)
        if not searchObj is None:
            # print(searchObj.group(1))
            print(line)
            track = searchObj.group(1)
            count = count+1
            fw.write(line)
            line = fo.readline()
            while line:
                if line.startswith("TRAIN"):
                    read_next = False
                    break
                if "上海虹桥," in line:
                    n_line = re.sub(r'上海虹桥,([0-9]),', lambda m: r'上海虹桥,' + track + ',', line)
                    print(line)
                    print(n_line)
                    fw.write(n_line)
                else:
                    fw.write(line)
                line = fo.readline()
    
    if read_next and line:
        fw.write(line)
        line = fo.readline()

print(count)
fo.close()
fw.close()