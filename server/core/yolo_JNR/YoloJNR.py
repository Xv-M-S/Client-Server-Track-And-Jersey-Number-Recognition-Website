from ultralytics import YOLO
import numpy as np
import os
# import streamlit as st
import time
import sys
current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
current_folder_path = os.path.dirname(current_file_path)
sys.path.append(current_folder_path)
from id_to_num import id_to_num
from visual_JN import main_video,main_image
import logging
# 是否开启DEBUG模式
# 设置日志级别为ERROR或CRITICAL
logging.getLogger("ultralytics").setLevel(logging.ERROR)

DEBUG = 1

def infer_JNR(data_path,R_Conf,F_Conf,user_id):
    current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
    current_folder_path = os.path.dirname(current_file_path)
    # 加载模型
    model = YOLO(os.path.join(current_folder_path,'../../models/AugSocv3PaperRoboMQY.pt'))  # 预训练的 YOLOv8n 模型
    detect_model = YOLO(os.path.join(current_folder_path,'../../models/DetectPaperRoboSvhnSocv3MQY_n.pt'))
    # crop保存路径【可选】
    # out_put_path = "./soccerNet-challenge/crops/"
    # 计算detect概率
    detect_save_txt = os.path.join(current_folder_path,"../../output",user_id,"JNR-detect.txt")
    f_detect = open(detect_save_txt,"w")
    count = 0
    detect = 0
    # 计算耗时
    time_cost_txt = os.path.join(current_folder_path,"../../output",user_id,"JNR-time.txt")
    f_timeCost =  open(time_cost_txt,"w")
    start_time = time.time()
    # 存储最终的结果
    id_num_txt = os.path.join(current_folder_path,"../../output",user_id,"id_num.txt")
    f_id_num =  open(id_num_txt,"w")
    final_map={}

    for id in os.listdir(data_path):
        image_dir = os.path.join(data_path,id)
        if not os.path.isdir(image_dir):
            continue
        detect_count = 0
        res_map = {} # 记录一个id序列中每个预测的数量
        for image in os.listdir(image_dir):
            image_path = os.path.join(image_dir,image)
            # 在图片上运行批量推理

            # 选择是否存储crop
            # out_dir = os.path.join(out_put_path,id)
            # result = model(source=image_path,task="detect",imgsz=256,save_crop=True,name=out_dir,conf=0.8,device=5)

            # 返回 Results 对象列表
            result = model(source=image_path,task="detect",imgsz=256,conf=R_Conf,device=7)
            count += 1
            # 边界框输出的 Boxes 对象
            boxes = result[0].boxes  
            # torch.tensor to string
            pre_label = boxes.cls
            temp = pre_label.cpu().numpy()
            pre_cls = ""
            if len(temp) == 1:
                pre_cls = str(int(temp[0]))
            if pre_cls != "": 
                detect += 1
            else:
                continue
            # detect判定是否真的含有球号
            detect_result = detect_model(source=image_path,task="detect",imgsz=256,conf=F_Conf,device=7)  # 返回 Results 对象列表
            is_exists_number = detect_result[0].boxes.cls.cpu().numpy()
            detect_cls = ""
            if len(is_exists_number)==1:
                detect_cls = str(int(is_exists_number[0]))
            if detect_cls == "0":
                detect_count += 1
            if pre_cls in res_map.keys():
                res_map[pre_cls]+=1
            else: 
                res_map[pre_cls]=0
        if not(res_map) or detect_count == 0:
            final_map[id] = -1
            f_id_num.write(id + " -1\n") 
            continue
        res_label = max(res_map, key=lambda x: res_map[x])
        print("res_label:" +  res_label)
        final_map[id] = int(res_label)
        f_id_num.write(id + " " + str(res_label) + "\n") 
    

    end_time = time.time()
    per_image_cost = round(float(end_time - start_time) * 1000.0/count,4)
    f_timeCost.write("DetectPaperRoboSvhnSocv3MQY_n_SoccerNet-test : "+str(per_image_cost)+"ms\n")
    f_timeCost.close()

    detect_rate = round((detect/count)*100,3)
    f_detect.write("DetectPaperRoboSvhnSocv3MQY_n_SoccerNet-test: "+str(detect_rate)+"%\n")
    f_detect.close()
    f_id_num.close()
    print(final_map)


# data_path = "/home/sxm/YoloTracking/YOLOv8-streamlit-app/results/video/detection_demo/crops/0"
# infer_JNR(data_path,0.7,0.7)