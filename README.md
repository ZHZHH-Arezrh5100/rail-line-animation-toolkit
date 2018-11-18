# 铁路运行略图生成工具
铁路运行略图自动生成工具<br>
([README in English](/README_EN.md))

## 简介
本工具用于制作铁路/轨道交通运行略图。运行略图是一种展现列车以图标的形式，按照时刻表，在线路简图上动态运行的视频。运行略图的截图示例如下图所示。<br>
![运行略图截图示例](/capture_sample.jpg)
动态运行略图的示例视频可以参照：[（尚未上传）av00000000](https://www.bilibili.com/video/av0)<br>
本工具提供了在Adobe After Effects CC中可以自动生成这种运行略图动画的脚本。脚本运行所需的时刻数据可以用Python脚本从12306上获取。<br>

## 如何使用本工具制作运行略图

1. **绘制线路图**<br>
用Visio或其它软件绘制背景线路图，如"[resources/bkgd_map.bmp](/resources/bkgd_map.bmp)"或"[resources/bkgd_map.vsdx](/resources/bkgd_map.vsdx)"。
2. **读取并填写定位点的坐标**<br>
定位点是用于列车位置关键帧的位置点。请参照"[script/locating_points_reference.bmp](/script/locating_points_reference.bmp)"和 "[script/stationId_trackId_reference.bmp](/script/stationId_trackId_reference.bmp)"。<br>
手动读取定位点坐标并将车站信息和定位点坐标填入"[script/train_animation_generator.jsx](/script/train_animation_generator.jsx)"。
3. **采集时刻表数据**<br>
首先，准备时刻表数据文件（包括列车数据和停站/经由点数据）。格式参照 "[schedule_data/schedule_data_final_down.csv](/schedule_data/schedule_data_final_down.csv)" 。数据说明如下。<br>
   ```javascript
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
   **如果是制作中国国铁的运行略图，可以使用"[schedule_data/query_schedule_12306.py](/schedule_data/query_schedule_12306.py)"从12306自动收集数据。可以添加两个车站之间的所有列车（输入两站的电报码，可以到moerail.ml网站查询），也可以输入车次一个一个添加。** <br>
4. **手动整理修改时刻表信息**<br>
自动采集的时刻表数据不包含停车股道、车型等信息，需要手动添加。一些必要的修改步骤如下。<br>
    * 添加经由点和端点。
    * 将多车次的列车拆分成多个列车。
    * 修改每个列车的每个停站的股道编号，避免停车的时候重叠。
    * 修改套跑列车的衔接时间。
    * 有必要的话，添加越行通过车站时间。
    * 查询并修改列车车型。
      * 可使用"[schedule_data/query_train_models.py](/schedule_data/query_train_models.py)"自动查询列车车型并修改数据。
    * 有必要的话，修改目的地类型。<br>
5. **生成视频**<br>
用AE打开"[AE_project_empty_templete.aep](/AE_project_empty_templete.aep)"，运行脚本"[script/train_animation_generator.jsx](/script/train_animation_generator.jsx)"以生成视频。

## 文件说明

## 注意
* 使用脚本前先看代码，可能要根据需要做一些更改。
* "[resources/icons/](/resources/icons)"中的列车车型图标下载自[Train Front View](http://www.trainfrontview.net)（或经过少许修改）。图标的版权归属于[Train Front View](http://www.trainfrontview.net)。如果要发布包含图标的视频，请先看这个网站上的要求。
