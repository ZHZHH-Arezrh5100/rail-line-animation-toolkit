// train_animation_generator.jsx
// Train Animation Generator 2nd EDITION Ver 2.31
// - Generate train animation by Adobe After Effects CC
// - 用 Adobe After Effects CC 生成列车运行略图动画
// - author: ZHZHH

// - environment: Adobe After Effects CC
// - prerequisites: 
// -- An existing project in After Effects.
// -- A folder item named as "icons".
// -- Train icon files in "icons" folder item.
// -- A composition named as "target", with a background image layer for the animation.
// -- (Recommended) Turn on "bold" font style in character frame.
// -- (Recommended) 1920x1080 (1:1).

// - updates:
// -- 2018-10-30: 实现添加图层、添加关键帧动画。
// -- 2018-10-31: 实现读取CSV列车时刻文件，自动添加车站定位点，批量生成关键帧动画。完成沪杭高速线定位点数据。
// -- 2018-11-01: 使用实际时刻进行测试，调整参数。
// -- 2018-11-02: 添加车次标志和目的地标志。
// -- 2018-11-04: Debug, png背景透明化。
// -- 2018-11-10: 实现一次添加多个文件。生成动画前将列车数据进行重新排序。
// -- 2018-11-13: 实现列车图标淡入淡出。


// ---- DATA & SETTINGS ---- //

// positions of locating points in every station (各车站的定位点位置)
// key format: (stationId + '_' + trackId) or (stationId + '_' + direction["U" / "D"](up/down) + ["I" / "M" / "O"](in/main/out))
// refer to "stationId_trackId_reference.bmp" and "locating_points_reference.bmp"
// (车站和股道编号参照 "stationId_trackId_reference.bmp"；定位点后缀含义参照 "locating_points_reference.bmp")
var locatingPoints = {
    // stations (实际车站)
    "SHH1_UI" : [1786, 228], "SHH1_UM" : [1786, 155], "SHH1_UO" : [1786, 089], "SHH1_DI" : [1815, 089], "SHH1_DM" : [1815, 155], "SHH1_DO" : [1815, 228], "SHH1_1" : [1737, 155], "SHH1_2" : [1863, 155], 
     "SHH1_3" : [1762, 155],  "SHH1_4" : [1838, 155],  "SHH1_5" : [1786, 155],  "SHH1_6" : [1815, 155],  "SHH1_7" : [1750, 180],  "SHH1_8" : [1850, 130], "SHH1_9" : [1774, 180], "SHH1_10" : [1826, 130], 
    "SHH2_UI" : [1689, 190], "SHH2_UM" : [1689, 155], "SHH2_UO" : [1659, 125], "SHH2_DI" : [1689, 125], "SHH2_DM" : [1689, 155], "SHH2_DO" : [1689, 190], "SHH2_20" : [1689, 155],
     "SJN_UI" : [1529, 352],  "SJN_UM" : [1597, 330],  "SJN_UO" : [1661, 309],  "SJN_DI" : [1670, 336],  "SJN_DM" : [1605, 357],  "SJN_DO" : [1537, 379],  "SJN_1" : [1586, 297],  "SJN_2" : [1616, 389],
     "JSB_UI" : [1329, 417],  "JSB_UM" : [1397, 395],  "JSB_UO" : [1461, 374],  "JSB_DI" : [1470, 401],  "JSB_DM" : [1406, 421],  "JSB_DO" : [1338, 443],  "JSB_1" : [1386, 362],  "JSB_2" : [1416, 454],
     "JSN_UI" : [1129, 481],  "JSN_UM" : [1197, 459],  "JSN_UO" : [1262, 438],  "JSN_DI" : [1270, 465],  "JSN_DM" : [1205, 486],  "JSN_DO" : [1137, 508],  "JSN_1" : [1186, 427],  "JSN_2" : [1216, 518],
     "JXN_UI" : [0927, 546],  "JXN_UM" : [0996, 524],  "JXN_UO" : [1061, 503],  "JXN_DI" : [1069, 530],  "JXN_DM" : [1005, 551],  "JXN_DO" : [0936, 573],  "JXN_1" : [0981, 478],  "JXN_2" : [1020, 597],
      "JXN_3" : [0989, 502],   "JXN_4" : [1013, 574],   "JXN_5" : [0959, 499],   "JXN_6" : [1049, 573],
     "TXG_UI" : [729, 610],  "TXG_UM" : [797, 588],  "TXG_UO" : [862, 568],  "TXG_DI" : [871, 595],  "TXG_DM" : [806, 615],  "TXG_DO" : [738, 638],  "TXG_1" : [787, 556],  "TXG_2" : [816, 647],
     "HNX_UI" : [530, 675],  "HNX_UM" : [598, 653],  "HNX_UO" : [662, 632],  "HNX_DI" : [670, 659],  "HNX_DM" : [606, 680],  "HNX_DO" : [538, 702],  "HNX_1" : [587, 621],  "HNX_2" : [616, 712],
     "YHG_UI" : [379, 724],  "YHG_UM" : [447, 701],  "YHG_UO" : [511, 680],  "YHG_DI" : [520, 707],  "YHG_DM" : [455, 728],  "YHG_DO" : [387, 750],  "YHG_1" : [436, 669],  "YHG_2" : [465, 760],
    "HZD1_UI" : [287, 951], "HZD1_UM" : [287, 880], "HZD1_UO" : [287, 812], "HZD1_DI" : [316, 812], "HZD1_DM" : [316, 880], "HZD1_DO" : [316, 951], "HZD1_1" : [238, 880], "HZD1_2" : [363, 880],
     "HZD1_3" : [263, 880],  "HZD1_4" : [339, 880],  "HZD1_5" : [287, 880],  "HZD1_6" : [316, 880],  "HZD1_7" : [250, 905],  "HZD1_8" : [351, 855], "HZD1_9" : [275, 905],  "HZD1_10" : [328, 855],
     "HZH_UI" : [086, 1030],  "HZH_UM" : [086, 1005],  "HZH_UO" : [086, 0937],  "HZH_DI" : [115, 0937],  "HZH_DM" : [115, 1005],  "HZH_DO" : [115, 1030],  "HZH_1" : [050, 1005],  "HZH_2" : [149, 1005],
      "HZH_3" : [086, 1005],   "HZH_4" : [115, 1005],
    // endpoint (边缘末端端点)
    "E1_UM" : [016, 574], "E1_DM" : [036, 554],
    "E2_UM" : [287, 1030], "E2_DM" : [316, 1030],
    "E3_UM" : [1786, 042], "E3_DM" : [1815, 042],
    "E4_UM" : [1659, 042], "E4_DM" : [1690, 042],
    // joint (转弯折点和分岔点)
    "J1_UM" : [086, 645], "J1_DM" : [115, 633],
    "J2_UM" : [086, 817], "J2_DM" : [115, 838],
    "J3_UM" : [287, 752], "J3_DM" : [316, 774],
    "J4_UM" : [1786, 269], "J4_DM" : [1815, 290],
    "J5_UM" : [1786, 228], "J5_DM" : [1815, 239],
};

// station_name to stationId
var stationNameToId = {
    "上海虹桥" : "SHH1",
    "上海虹桥2" : "SHH2",
    "松江南" : "SJN",
    "金山北" : "JSB",
    "嘉善南" : "JSN",
    "嘉兴南" : "JXN",
    "桐乡" : "TXG",
    "海宁西" : "HNX",
    "余杭" : "YHG",
    "杭州东" : "HZD1",
    "杭州" : "HZH",
    "E1" : "E1",
    "E2" : "E2",
    "E3" : "E3",
    "E4" : "E4",
    "J1" : "J1",
    "J2" : "J2",
    "J3" : "J3",
    "J4" : "J4",
    "J5" : "J5",
};      

// the time of entering a station or departing from a station (进出站用时)
var transitTimeSec = {
    "SHH1" : 0.65,
    "SHH2" : 0.3,
    "SJN" : 0.65,
    "JSB" : 0.65,
    "JSN" : 0.65,
    "JXN" : 0.65,
    "TXG" : 0.65,
    "HNX" : 0.65,
    "YHG" : 0.65,
    "HZD1" : 0.65,
    "HZH" : 0.65,
    "E1" : 0.65,
    "E2" : 0.65,
    "E3" : 0.65,
    "E4" : 0.65,
    "J1" : 0.65,
    "J2" : 0.65,
    "J3" : 0.65,
    "J4" : 0.65,
    "J5" : 0.65,
};

// the actual time when the video begin (视频开始的现实时间)
var startTime = "05:00";

// the actual time when the video end (视频结束的现实时间)
var endTime = "25:00";

// the time length the video (视频时长)
var aniLengthSec = 5.0 * 60;


// ---- CLASSES & ENUMS ---- //

// info of a one-way train (单程车次信息)
function Train(_params){                            // input: string _params[0..5]
    this.trainName = _params[1];                    // train name shown on icon (图标上显示的车次或种别) e.g.: "G7302"
    this.destination = _params[2];                  // destination shown on icon (图标上显示的目的地) e.g.: "上海虹桥"
    this.iconId = _params[3];                       // id of icon (车型图标ID) e.g.: "crh380a"
    this.classColor = ColorType[_params[4]];        // color of train class (种别标识色) e.g.: "BLUE"
    this.destinationColor = ColorType[_params[5]];  // color of destination type (目的地种类标识色) e.g.: "PURPLE"
    this.waypoints = [];                            // waypoints (stop points) info of the train (列车经由点信息)
    this.sortIndex = 0;                             // index for sort trains (用于排序的索引)
}

// info of a waypoint (经由点信息)
function Waypoint(_params){                         // input: string _params[0..6]
    this.type = WaypointType[_params[0]];           // waypoint type (经由点类型) e.g.: "STOP"
    this.arrTime = _params[1];                      // arrival time or pass time (到站时间或通过时间) e.g.: "8:00"
    this.depTime = _params[2];                      // departure time (发车时间) e.g.: "8:03"
    this.stationId = stationNameToId[_params[3]];   // id of the station (车站ID) e.g.: "HZD1"
    this.trackId = _params[4];                      // id of the track (停车股道ID) e.g.: "1"
    this.inDirection = _params[5];                  // direction of arrival (进站方向) U/D e.g.: "U"
    this.outDirection = _params[6];                 // direction of departure (出站方向) U/D e.g.: "U"
}

// waypoint type (经由点类型)
var WaypointType = {
    PASS : 0,       // pass without stop (通过站)
    STOP : 1,       // stop at a station (经停站)
    INITIAL : 2,    // first station (始发站)
    TERMINAL : 3,   // last station (终到站)
    TRAIN : 255,     // not a waypoint (非经由点)
};

// color type (颜色类型)
var ColorType = {
    // by color name
    RED : [1.0, 0.0, 0.0],
    GREEN : [0.0, 1.0, 0.0],
    BLUE : [0.0, 0.0, 1.0],
    YELLOW : [1.0, 1.0, 0.0],
    CYAN : [0.0, 1.0, 1.0],
    PURPLE : [1.0, 0.0, 1.0],
    // background color of train-class
    G : [0.0, 0.0, 0.5],  // blue
    D : [0.5, 0.5, 1.0],  // light blue
    C : [0.0, 0.5, 0.5],  // cyan
    S : [1.0, 0.0, 1.0],  // purple
    Z : [1.0, 0.5, 0.0],  // orange
    T : [0.8, 0.8, 0.0],  // yellow
    K : [1.0, 0.0, 0.0],  // red
    0 : [0.0, 0.3, 0.0],  // dark green
    // font color of train-class
    TRAIN_CLASS_TEXT : [1.0, 1.0, 1.0],
    // font color of destination
    TO_OTHER_LINES : [0.0, 0.5, 0.0],
    TO_LONG_DISTANCE : [0.0, 0.8, 0.0],
    TO_MAIN_TERMINAL : [0.5, 0.0, 0.5],
    TO_SUB_TERMINAL : [1.0, 0.0, 1.0],
    TO_HALFWAY_STOP : [0.6, 0.6, 1.0],
    // stroke color
    STROKE : [1.0, 1.0, 1.0],
};


// ---- SCRIPT BEGIN ---- //

// check environment
if (BridgeTalk.appName != "aftereffects"){
    alert("This script can only run with Adobe After Effects CC.\nPlease Open a project and run in After Effects.");
    throw new Error('Not in AE.');
}

// load icons and target composition
var icons = null;
var comp = null;
for (var i = 1; i <= app.project.numItems; i++){
    if (app.project.item(i) instanceof FolderItem){
        if (app.project.item(i).name == "icons"){
            icons = app.project.item(i);
        }
    }
    if (app.project.item(i) instanceof CompItem){
        if (app.project.item(i).name == "target"){
            comp = app.project.item(i);
        }
    }
}
if (icons == null){
    alert("Icons folder not found!");
    throw new Error('Item not found.');
}
if (comp == null){
    alert("Target composition not found!");
    throw new Error('Item not found.');
}

// initiate time setting
var startActualSec = time2ActualSec(startTime);
var timeRate = (time2ActualSec(endTime) - time2ActualSec(startTime)) / aniLengthSec;

// import trains
clearOutput();
writeLn("Please open a schedule data file.");
writeLn("请打开列车时刻的CSV文件。");
var fScheduleDatas = File.openDialog("Open CSV schedule data file (打开CSV列车时刻文件)", "CSV:*.csv",true);
var fScheduleData = null;
if (fScheduleDatas == null){
    alert("No file avalible!");
    throw new Error('No file avalible.');
}
var line;
var params;
var trains = [];
for (var fId in fScheduleDatas){
    fScheduleData = fScheduleDatas[fId];
    if (fScheduleData == null){
        continue;
    }
    var nTrain = null;
    var nWaypoints = [];
    if (fScheduleData.open("r")){
        while (!fScheduleData.eof){
            line = fScheduleData.readln();
            params = line.split(",");
            if (params.length >= 6){
                if (params[0] == "TRAIN"){  // add a line of train
                    if (nTrain != null) {
                        nTrain.waypoints = nWaypoints;
                    }
                    nTrain = new Train(params);
                    trains.push(nTrain);
                    nWaypoints = []
                }
                else{
                    if (params.length >= 7){  // add a line of waypoint
                        nWaypoint = new Waypoint(params);
                        if (nWaypoint.stationId != undefined)  // ignore the station if it's not in stationNameToId
                            nWaypoints.push(nWaypoint);
                            if (nWaypoint.stationId == "SHH1" || nWaypoint.stationId == "SHH2")
                                if (nTrain != null)
                                    nTrain.sortIndex = time2AniSec(nWaypoint.arrTime);  // sort by the time arriving Shanghai Hongqiao
                    }
                }
            }
        }
        if (nTrain != null) {
            nTrain.waypoints = nWaypoints;
        }
        fScheduleData.close();
    }
    else{
        alert("Failed to open file!");
    }
}
clearOutput();
writeLn(trains.length + " train(s) imported.");
writeLn("已导入列车：" + trains.length);
alert("Click OK to generate train animation.");

// add trains
trains.sort(function(a, b) {return a.sortIndex - b.sortIndex;});
clearOutput();
writeLn("Generating train animation...");
writeLn("正在生成列车运行略图动画...");
writeLn("Press Esc to abort.");
for (var trainId in trains){
    addTrain(trains[trainId]);
}

clearOutput();
writeLn("Done.");
writeLn("生成完毕。");


// ---- FUNCTIONS ---- //

// add an animation of a train
function addTrain(train){
    
    // set locating points
    var waypoint = null;
    var timeArray = [];
    var posArray = [];
    var initialTime = aniLengthSec;  // appearing time
    var terminalTime = 0;            // disappearing time
    for (var waypointId in train.waypoints){
        waypoint = train.waypoints[waypointId];
        if (!(waypoint instanceof Waypoint)){
            alert("Invalid waypoint!");
            return;
        }
        
        var arrTimeSec = time2AniSec(waypoint.arrTime); // arrival time in animation
        var depTimeSec = time2AniSec(waypoint.depTime); // departure in animation
        if (initialTime > arrTimeSec){
            initialTime = arrTimeSec;   // min
            if (waypoint.type == WaypointType.INITIAL)
                initialTime -= 0.05;
        }
        if (terminalTime < depTimeSec){
            terminalTime = depTimeSec;  // max
            if (waypoint.type == WaypointType.TERMINAL)
                terminalTime += 0.05;
        }
        
        // set locating points
        switch (waypoint.type){
        case WaypointType.PASS:
            // pass point
            timeArray.push(arrTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.inDirection + "M"]);
            break;
        case WaypointType.STOP:
            // entering siding
            timeArray.push(arrTimeSec - transitTimeSec[waypoint.stationId]);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.inDirection + "I"]);
            // stopping at track
            timeArray.push(arrTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            // departing from track
            timeArray.push(depTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            // leaving from track
            timeArray.push(depTimeSec + transitTimeSec[waypoint.stationId]);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.outDirection + "O"]);
            break;
        case WaypointType.INITIAL:
            // appearing at track
            timeArray.push(arrTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            // departing from track
            timeArray.push(depTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            // leaving from track
            timeArray.push(depTimeSec + transitTimeSec[waypoint.stationId]);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.outDirection + "O"]);
            break;
        case WaypointType.TERMINAL:
            // entering siding
            timeArray.push(arrTimeSec - transitTimeSec[waypoint.stationId]);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.inDirection + "I"]);
            // stopping at track
            timeArray.push(arrTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            // disappearing from track
            timeArray.push(depTimeSec);
            posArray.push(locatingPoints[waypoint.stationId + '_' + waypoint.trackId]);
            break;
        default:
            // do nothing
        }
    }
    
    // add the graph of the train
    var nLayer = null;
    nLayer = addTrainGraph(train, initialTime, terminalTime);
    
    // add time of key frames and positions at key frames
    nLayer.property("Transform").property("Position").setValuesAtTimes(timeArray, posArray);
    // set spatial interpolation type to linear (by set a tangents of 0)
    for (var i = 1; i <= nLayer.property("Transform").property("Position").numKeys; i++) {
        nLayer.property("Transform").property("Position").setSpatialTangentsAtKey(i, [0, 0, 0]);
    }
    // add time of key frames and opacities at key frames
    nLayer.property("Transform").property("Opacity").setValuesAtTimes([initialTime, initialTime + 0.1, terminalTime - 0.1, terminalTime], [0, 100, 100, 0]);
}

// add the graph of a train
function addTrainGraph(train, initialTime, terminalTime){
    // add train icon layer
    var iconLayer = null;
    var iconItem = null;
    for (var i = 1; i <= icons.numItems; i++){
        if (icons.item(i) instanceof FootageItem){
            if (icons.item(i).name == train.iconId + ".png"){
                iconItem = icons.item(i);
                break;
            }
        }
    }
    if (iconItem == null){
        iconItem = icons.item(1);
    }
    iconLayer = comp.layers.add(iconItem);
    iconLayer.name = "Icon";
    var colorKeyEffect = iconLayer.property("Effects").addProperty("ADBE Color Key");  // set transparent background
    colorKeyEffect.property("ADBE Color Key-0001").setValue([1, 0, 1, 1]);
    colorKeyEffect.property("ADBE Color Key-0002").setValue(5);

    // add train class label layer
    var classShapeLayer = null;
    classShapeLayer = comp.layers.addShape();
    classShapeLayer.name = "Label";
    var rectCont = classShapeLayer.property("Contents").addProperty("ADBE Vector Shape - Rect");
    rectCont.property("Size").setValue([45, 14]);
    rectCont.property("Position").setValue([0, -27]);
    rectCont.property("Roundness").setValue(10);
    var fillCont = classShapeLayer.property("Contents").addProperty("ADBE Vector Graphic - Fill");
    fillCont.property("Color").setValue(train.classColor);
    var strokeCont = classShapeLayer.property("Contents").addProperty("ADBE Vector Graphic - Stroke");
    strokeCont.property("Color").setValue(ColorType["STROKE"]);
    strokeCont.property("Stroke Width").setValue(3);

    // add train class text layer
    var classTextLayer = null;
    classTextLayer = comp.layers.addText(train.trainName);
    classTextLayer.name = "Train Class";
    var classTextDoc = classTextLayer.property("Text").property("Source Text").value;
    classTextDoc.fillColor = ColorType["TRAIN_CLASS_TEXT"];
    classTextDoc.font = "Segoe UI";
    classTextDoc.fontSize = 14;
    classTextDoc.applyFill = true;
    classTextDoc.applyStroke = false;
    classTextLayer.property("Text").property("Source Text").setValue(classTextDoc);
    var textPos = classTextLayer.property("Transform").property("Position").value;
    classTextLayer.property("Transform").property("Position").setValue([textPos[0], textPos[1] - 22]);

    // add destination text layer
    var destinationTextLayer = null;
    destinationTextLayer = comp.layers.addText(train.destination);
    destinationTextLayer.name = "Destination";
    var destinationTextDoc = destinationTextLayer.property("Text").property("Source Text").value;
    destinationTextDoc.fillColor = train.destinationColor;
    destinationTextDoc.strokeColor = ColorType["STROKE"];
    destinationTextDoc.font = "SimHei";  // 黑体
    destinationTextDoc.fontSize = 18;
    destinationTextDoc.applyFill = true;
    destinationTextDoc.applyStroke = true;
    destinationTextDoc.strokeWidth = 3;
    destinationTextDoc.strokeOverFill = false;
    destinationTextLayer.property("Text").property("Source Text").setValue(destinationTextDoc);
    textPos = destinationTextLayer.property("Transform").property("Position").value;
    destinationTextLayer.property("Transform").property("Position").setValue([textPos[0], textPos[1] + destinationTextDoc.fontSize + 20]);
    // *: It seems to be not possible to set a "bold" font style by scripting. So, turn on the "bold" style in "Character" frame before running this script.

    // compose layers
    comp.layers.precompose([1, 2, 3, 4], train.trainName);
    comp.layer(1).inPoint = initialTime;
    comp.layer(1).outPoint = terminalTime;
    return comp.layer(1);
}

// transfer time string "HH:MM" to seconds in animation
function time2AniSec(timeString){    
    var actualSec = time2ActualSec(timeString);
    if (actualSec == 0){
        return 0;
    }
    else{
        return (actualSec - startActualSec) / timeRate;
    }
}

// transfer time string "HH:MM" to actual seconds
function time2ActualSec(timeString){
    var timePart = timeString.split(":");
    if (timePart.length == 2){
        return (parseInt(timePart[0]) * 60 + parseInt(timePart[1])) * 60;
    }
    else{
        return 0;
    }
}
