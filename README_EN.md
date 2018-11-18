# Rail Line Animation Toolkits
Automatic train animation generator
（[中文版README](/README.md)）

## Introduction
This is a toolkit for making Rail Line Animation of railway/metro. The Rail Line Animation (or train animation) is a kind of video in which trains is shown as icons moving on the railway map according to the schedule. The capture of a Rail Line Animation is shown below.<br>

Here is a Rail Line Animation video: [(Not uploaded yet) av00000000](https://www.bilibili.com/video/av0)<br>

This toolkit provides a script for generating Rail Line Animation in Adobe After Effects CC. The data for the script can be queried from 12306.cn by Python.<br>

## How To Make a train animation <br>

1. **Draw a railway line map**<br>
Use Visio or other software to draw a background map, like "[resources/bkgd_map.bmp](/resources/bkgd_map.bmp)" or "[resources/bkgd_map.vsdx](/resources/bkgd_map.vsdx)".<br>
2. **Read and fill in the position of locating points**<br>
The locating points is the key position of the trains. Refer to "[script/locating_points_reference.bmp](/script/locating_points_reference.bmp)" and "[script/stationId_trackId_reference.bmp](/script/stationId_trackId_reference.bmp)".<br>
Read the position (x, y) of each locating point manually (use mspaint), and fill all station data and position data into "[script/train_animation_generator.jsx](/script/train_animation_generator.jsx)"<br>
3. **Get the schedule data**<br>
The first step is to prepare the schedule files, which includes all information of the trains (train name, destination, train class, train model icon...) and information of the stops of each train (arrival time, departure time, station name, track...). Refer to "[schedule_data/schedule_data_final_down.csv](/schedule_data/schedule_data_final_down.csv)" for the format of the schedule data file. All necessary data is listed below.<br>
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
   **If the train schedule you need is on 12306 (China Railway), use "[schedule_data/query_schedule_12306.py](/schedule_data/query_schedule_12306.py)" to collect data from 12306.cn automatically. You can add all trains between two stations by input the station code of "from" and "to" station, or add trains by train name (train code) one by one.**<br>
4. **Modify the schedule data manually**<br>
The data got by query_schedule_12306.py does not include some information such as track, train model type... These information can only be added manually. Some necessary modification is listed below.<br>
    * Add way points (where the line turns, or the end point at the edge of the map).
    * For the trains which have more than one train name, split them to two or more trains.
    * Modify the track number of each stop of each train. Avoid overlapping.
    * For the trains which use the same vehicle, change the time when they disappear and appear.
    * Add the time of passing a station if necessary.
    * Check and modify the train model of each trains.
      * For trains of China Railway, use "[schedule_data/query_train_models.py](/schedule_data/query_train_models.py)" to query the vehicle models from moerail.ml, and modify the train icons in the schedule data files.
    * Modify the destination type if necessary.<br>
5. **Generate the video**<br>
Open "[AE_project_empty_templete.aep](/AE_project_empty_templete.aep)" in After Effects, add the background map, and run "[script/train_animation_generator.jsx](/script/train_animation_generator.jsx)" to generate the video.<br>

## File Description <br>

## Notice <br>
* Read the script code before using it. Some minor changes might be necessary for other railway lines. <br>
* The train icons in "[resources/icons/](/resources/icons)" is downloaded from [Train Front View](http://www.trainfrontview.net/en/index.htm) (or with some minor changes). The copyright of the icons are owned by [Train Front View](http://www.trainfrontview.net/en/index.htm). Please check the website if you want to publish the video with the icons. <br>
