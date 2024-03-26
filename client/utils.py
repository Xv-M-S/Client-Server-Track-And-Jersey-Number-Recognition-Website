#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     client.py
   @Author:        Shi Xumao
   @Date:          2024/3/19
   @Description:
-------------------------------------------------
"""
from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import io
import config
import os
import subprocess
import requests
import secrets
import string



def generate_random_id(length):
    characters = string.ascii_uppercase + string.digits
    random_id = ''.join(secrets.choice(characters) for _ in range(length))
    return random_id


def infer_uploaded_image(conf, method , set_rec_confidence, set_filter_confidence):
    """
    Execute inference for uploaded image
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_img = st.sidebar.file_uploader(
        label="Choose an image...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )
    # 清除会话状态
    if "video" in st.session_state or len(st.session_state)==0:
        sid = st.session_state["session_id"]
        st.session_state.clear()
        st.session_state["session_id"] = sid
        st.session_state["image"] = "runing"
        print(st.session_state)
    

    if source_img:
        if "source_image" not in st.session_state:
            st.session_state["source_image"] = source_img
        if st.session_state["source_image"] != source_img:
            sid = st.session_state["session_id"]
            st.session_state.clear()
            st.session_state["session_id"] = sid
            st.session_state["source_image"] = source_img
            print(st.session_state)
        source_image = Image.open(source_img)
        # 保存上传的图片到指定位置

        source_image.save(os.path.join("./input",st.session_state["session_id"],"demo.png"))
        # adding the uploaded image to the page with caption
        st.image(
            image=source_img,
            caption="Uploaded Image",
            use_column_width=True
        )
    run_JNR = False
    if source_img:
        if st.button("Execut Player tracking"):
            # 清理工作，清理后续的键，以防止在上传不同图片时显示了其他结果
            if "det_image" in st.session_state:
                del st.session_state["det_image"]
            if "visual_image" in st.session_state:
                del st.session_state["visual_image"]
            with st.spinner("Running..."):
                # 构建http请求
                url = 'http://120.46.142.89:8080/track_image'
                # 构造请求数据
                data = {
                    'user_id':st.session_state["session_id"],
                    'image':'running', # 特殊标识
                    'tracking_method': method,
                    'show_confidence': conf,
                    # 'filter_confidence': set_filter_confidence,
                    # 'recognition_confidence': set_rec_confidence
                }
                # 构造文件数据
                files = {
                    'original_image': open(os.path.join("./input",st.session_state["session_id"],"demo.png"), 'rb')
                }

                # 执行resquest请求
                response = requests.post(url, data=data, files=files)
                # 处理返回的图片
                # 检查响应状态码
                if response.status_code == 200:
                    # 提取图片数据
                    image_data = response.content
                    # 保存图片数据到本地文件
                    with open(os.path.join('./output',st.session_state["session_id"],'track_demo.png'), 'wb') as file:
                        file.write(image_data)
                        print('图片保存成功！')
                else:
                    print('请求失败，状态码：', response.status_code)
                      
                res_plotted = os.path.join('./output',st.session_state["session_id"],'track_demo.png')
                st.session_state["det_image"] = res_plotted
                    

        # if run_JNR:
        if "det_image" in st.session_state:
            res_plotted = st.session_state["det_image"]
            st.image(res_plotted,
                        caption="Detected Image",
                        use_column_width=True)
        
            if st.button("Execut Jersey number recognition"):
                with st.spinner("Running..."):
                    # 构建http请求
                    url = 'http://120.46.142.89:8080/JNR_image'
                    # 构造请求数据
                    data = {
                        'user_id':st.session_state["session_id"],
                        'Image_JNR':'running', # 特殊标识
                        # 'tracking_method': method,
                        # 'show_confidence': conf,
                        'filter_confidence': set_filter_confidence,
                        'recognition_confidence': set_rec_confidence
                    }
                    # 执行resquest请求
                    response = requests.post(url, data=data)
                    # 处理返回的图片
                    # 检查响应状态码
                    if response.status_code == 200:
                        # 提取图片数据
                        image_data = response.content
                        # 保存图片数据到本地文件
                        save_path = os.path.join('./output',st.session_state["session_id"],'JNR_demo.png')
                        with open(save_path, 'wb') as file:
                            file.write(image_data)
                            print('图片保存成功！')
                    else:
                        print('请求失败，状态码：', response.status_code)
                    st.session_state["visual_image"] = save_path
            if 'visual_image' in st.session_state:
                st.image(st.session_state["visual_image"],
                        caption="Detected and Recognized Image",
                        use_column_width=True)

    
                    


def infer_uploaded_video(conf, method, set_rec_confidence, set_filter_confidence):
    """
    Execute inference for uploaded video
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="Choose a video..."
    )
    # 清除会话状态
    if "image" in st.session_state or len(st.session_state)==0:
        sid = st.session_state["session_id"]
        st.session_state.clear()
        st.session_state["session_id"] = sid
        st.session_state["video"] = "runing"
        print(st.session_state)


    if source_video:
        if "source_video" not in st.session_state:
            st.session_state["source_video"] = source_video
        if st.session_state["source_video"] != source_video:
            sid = st.session_state["session_id"]
            st.session_state.clear()
            st.session_state["session_id"] = sid
            st.session_state["source_video"] = source_video
            print(st.session_state)
        # 保存上传的视频到指定位置
        g = io.BytesIO(source_video.read())
        temporary_location = os.path.join("./input",st.session_state["session_id"],"demo.mp4")

        with open(temporary_location,"wb") as out:
            out.write(g.read())

        # 演示上传的视频
        st.video(source_video)

    run_JNR = False
    if source_video:
        if st.button("Execut Player tracking"):
            # 清理工作，清理后续的键，以防止在上传不同图片时显示了其他结果
            if "det_video" in st.session_state:
                del st.session_state["det_video"]
            if "visual_video" in st.session_state:
                del st.session_state["visual_video"]
            with st.spinner("Running..."):
                # 构建http请求
                url = 'http://120.46.142.89:8080/track_video'
                # 构造请求数据
                data = {
                    'user_id':st.session_state["session_id"],
                    'video':'running', # 特殊标识
                    'tracking_method': method,
                    'show_confidence': conf,
                    # 'filter_confidence': set_filter_confidence,
                    # 'recognition_confidence': set_rec_confidence
                }
                # 构造文件数据
                files = {
                    'original_video': open(os.path.join("./input",st.session_state["session_id"],"demo.mp4"), 'rb')
                }

                # 执行resquest请求
                response = requests.post(url, data=data, files=files)
                # 处理返回的图片
                # 检查响应状态码
                if response.status_code == 200:
                    # 提取图片数据
                    image_data = response.content
                    # 保存图片数据到本地文件
                    with open(os.path.join('./output',st.session_state["session_id"],'track_demo.mp4'), 'wb') as file:
                        file.write(image_data)
                        print('图片保存成功！')
                else:
                    print('请求失败，状态码：', response.status_code)
                      
                res_plotted = os.path.join('./output',st.session_state["session_id"],'track_demo.mp4')
                st.session_state["det_video"] = res_plotted
                
        if "det_video" in st.session_state:
            st.video(st.session_state["det_video"])
            if st.button("Execut Jersey number recognition"):
                with st.spinner("Running..."):
                    # 构建http请求
                    url = 'http://120.46.142.89:8080/JNR_video'
                    # 构造请求数据
                    data = {
                        'user_id':st.session_state["session_id"],
                        'Video_JNR':'running', # 特殊标识
                        # 'tracking_method': method,
                        # 'show_confidence': conf,
                        'filter_confidence': set_filter_confidence,
                        'recognition_confidence': set_rec_confidence
                    }
                    # 执行resquest请求
                    response = requests.post(url, data=data)
                    # 处理返回的图片
                    # 检查响应状态码
                    if response.status_code == 200:
                        # 提取图片数据
                        video_data = response.content
                        # 保存图片数据到本地文件
                        save_path = os.path.join('./output',st.session_state["session_id"],'JNR_demo.mp4')
                        with open(save_path, 'wb') as file:
                            file.write(video_data)
                            print('图片保存成功！')
                    else:
                        print('请求失败，状态码：', response.status_code)
                    st.session_state["visual_video"] = save_path
            if 'visual_video' in st.session_state:
                st.video(st.session_state["visual_video"])

