
Sample schedule data:

1. 从12306获得的原始数据，使用“query_schedule_12306.py”。
	schedule_data_raw_down.csv
	schedule_data_raw_up.csv

(以下是漫长的手动调整)

2. 修改杭州东和嘉兴南的各个停靠列车的停靠股道。对杭州站的换向列车进行车次拆分。
	schedule_data_edited_down_1104.csv
	schedule_data_edited_up_1104.csv

3. 修改杭州的各个停靠列车的停靠股道。修改杭州站套跑列车的时刻。
	schedule_data_edited_down_1105.csv
	schedule_data_edited_up_1105.csv

4. 修改上海虹桥综合场列车的股道，并添加J5和E4定位点。
	schedule_data_edited_down_1106.csv
	schedule_data_edited_up_1106.csv


5. 修改部分上海虹桥高速场列车的股道(可查询到的)。
	schedule_data_edited_down_1108.csv
	schedule_data_edited_up_1108.csv

6. 修改上海虹桥高速场列车的股道(根据动画情况排布，尽量避免重叠)。
	schedule_data_edited_down_1109.csv
	schedule_data_edited_up_1109.csv

7. 使用“query_schedule_12306.py”添加套跑车次，调整股道避免重叠。
	schedule_data_edited_down_1110.csv
	schedule_data_edited_up_1110.csv
	schedule_data_edited_other_1110.csv

8. 修改越行通过时间。
	schedule_data_edited_down_1110-02.csv
	schedule_data_edited_up_1110-02.csv
	schedule_data_edited_other_1110-02.csv

9. 查询车型，使用“query_train_models.py”。
	schedule_data_edited_down_1111.csv
	schedule_data_edited_up_1111.csv
	schedule_data_edited_other_1111.csv

10. 修改目的地类别。
	schedule_data_final_down.csv
	schedule_data_final_up.csv
	schedule_data_final_other.csv