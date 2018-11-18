# Rail Line Animation Toolkits <br>铁路运行略图生成工具
Automatic train animation generator <br>铁路运行略图自动生成工具
## Introduction <br>简介
本工具用于制作铁路/轨道交通运行略图


## How To Make a train animation <br>如何使用本工具制作运行略图

1. **Draw a railway line map 绘制线路图**<br>
Use Visio or other software to draw a background map, like "resources/bkgd_map.bmp" or "resources/bkgd_map.vsdx".<br>
用Visio或其它软件绘制背景线路图，如"resources/bkgd_map.bmp"或"resources/bkgd_map.vsdx"。
1. **Read and fill in the position of locating points 读取并填写定位点的坐标**<br>
The locating points is the key position of the trains. Refer to "script/locating_points_reference.bmp" and "script/stationId_trackId_reference.bmp".<br>
定位点是用于列车位置关键帧的位置点。请参照 "script/locating_points_reference.bmp" 和 "script/stationId_trackId_reference.bmp"。<br>
Read the position (x, y) of each locating point manually (use mspaint), and fill all station data and position data into "script/train_animation_generator.jsx"<br>
手动读取定位点坐标并将车站信息和定位点坐标填入"script/train_animation_generator.jsx"。
1. **Get the schedule data 采集时刻表数据**<br>
The first step is to prepare the schedule files, which includes all information of the trains (train name, destination, train class, train model icon...) and information of the stops of each train (arrival time, departure time, station name, track...). Refer to "schedule_data/schedule_data_final_down.csv" for the format of the schedule data file. All necessary data is listed below.<br>
首先，准备时刻表数据文件（包括列车数据和停站/经由点数据）。格式参照 "schedule_data/schedule_data_final_down.csv" 。数据说明如下。<br>
```
// info of a one-way train (单程车次信息)
TRAIN = _params[0];                        // "TRAIN"
trainName = _params[1];                    // train name shown on icon (图标上显示的车次或种别) e.g.: "G7302"
destination = _params[2];                  // destination shown on icon (图标上显示的目的地) e.g.: "上海虹桥"
iconId = _params[3];                       // id of icon (车型图标ID) e.g.: "crh380a"
classColor = ColorType[_params[4]];        // color of train class (种别标识色) e.g.: "BLUE"
destinationColor = ColorType[_params[5]];  // color of destination type (目的地种类标识色) e.g.: "PURPLE"
// info of a waypoint (经由点信息)
type = WaypointType[_params[0]];           // waypoint type (经由点类型) e.g.: "STOP"
arrTime = _params[1];                      // arrival time or pass time (到站时间或通过时间) e.g.: "8:00"
depTime = _params[2];                      // departure time (发车时间) e.g.: "8:03"
stationId = stationNameToId[_params[3]];   // id of the station (车站ID) e.g.: "HZD1"
trackId = _params[4];                      // id of the track (停车股道ID) e.g.: "1"
inDirection = _params[5];                  // direction of arrival (进站方向) U/D e.g.: "U"
outDirection = _params[6];                 // direction of departure (出站方向) U/D e.g.: "U"
```
**If the train schedule you need is on 12306 (China Railway), use "schedule_data/query_schedule_12306.py" to collect data from 12306.cn automatically. You can add all trains between two stations by input the station code of "from" and "to" station, or add trains by train name (train code) one by one.<br>
如果是制作中国国铁的运行略图，可以使用"schedule_data/query_schedule_12306.py"从12306自动收集数据。可以添加两个车站之间的所有列车（输入两站的电报码，可以到moerail.ml网站查询），也可以输入车次一个一个添加。** <br>

1. **Modify the schedule data manually 手动整理修改时刻表信息**<br>
The data got by query_schedule_12306.py does not include some information such as track, train model type... These information can only be added manually. Some necessary modification is listed below.<br>
自动采集的时刻表数据不包含停车股道、车型等信息，需要手动添加。一些必要的修改步骤如下。<br>
  * Add way points (where the line turns, or the end point at the edge of the map). 添加经由点和端点。
  * For the trains which have more than one train name, split them to two or more trains. 将多车次的列车拆分成多个列车。
  * Modify the track number of each stop of each train. Avoid overlap. 修改每个列车的每个停站的股道编号，避免停车的时候重叠。
  * For the trains which use the same vehicle, change the time when they disappear and appear. 修改套跑列车的衔接时间。
  * Add the time of passing a station if necessary. 有必要的话，添加越行通过车站时间。
  * Check and modify the train model of each trains. 查询并修改列车车型。
    * For trains of China Railway, use "schedule_data/query_train_models.py" to query the vehicle models from moerail.ml, and modify the train icons in the schedule data files. 可使用"schedule_data/query_train_models.py"自动查询列车车型并修改数据。
  * Modify the destination type if necessary. 有必要的话，修改目的地类型。
1. **Generate the video 生成视频**<br>
Open "AE_project_empty_templete.aep" in After Effects, add the background map, and run "script/train_animation_generator.jsx" to generate the video.<br>
用AE打开"AE_project_empty_templete.aep"，运行脚本"script/train_animation_generator.jsx"以生成视频。
## File Description <br>文件说明

## Notice <br>注意
