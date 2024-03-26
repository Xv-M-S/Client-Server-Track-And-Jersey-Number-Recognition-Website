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
from pathlib import Path
from PIL import Image
import streamlit as st
import config
from utils import infer_uploaded_image, infer_uploaded_video,generate_random_id
import secrets
import string
import os

# 为每一段会话，生成一个session_id
if "session_id" not in st.session_state:
    session_id = generate_random_id(10)
    st.session_state["session_id"] = session_id
# 创建对应的文件夹
if not os.path.exists(os.path.join("./input",st.session_state["session_id"])):
    os.makedirs(os.path.join("./input",st.session_state["session_id"]))
if not os.path.exists(os.path.join("./output",st.session_state["session_id"])):
    os.makedirs(os.path.join("./output",st.session_state["session_id"]))
# setting page layout
st.set_page_config(
    page_title="Interactive Interface for Player tracking and Jersey number recognition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.title("Interactive Interface for Player tracking and Jersey number recognition")

# sidebar
st.sidebar.header("Track Model Config")

track_way = st.sidebar.selectbox(
    "Select Method",
    config.DETECTION_METHOD_LIST
)

show_confidence = st.sidebar.selectbox(
    "show Confidence",
    ["True","False"]
)
confidence = True if show_confidence == "True" else False

# sidebar
st.sidebar.header("Recognition Model Config")

set_rec_confidence = float(st.sidebar.slider(
    "Set Recognition Confidence", 30, 100, 70)) / 100

set_filter_confidence = float(st.sidebar.slider(
    "Set Filter Confidence", 30, 100, 70)) / 100


# image/video options
st.sidebar.header("Image/Video Config")
source_selectbox = st.sidebar.selectbox(
    "Select Source",
    config.SOURCES_LIST
)


if source_selectbox == config.SOURCES_LIST[0]: # Image
    infer_uploaded_image(confidence, track_way, set_rec_confidence, set_filter_confidence)
elif source_selectbox == config.SOURCES_LIST[1]: # Video
    infer_uploaded_video(confidence, track_way, set_rec_confidence, set_filter_confidence)
elif source_selectbox == config.SOURCES_LIST[2]: # Webcam
    st.error("Currently only 'Image' and 'Video' source are implemented")
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")


if st.sidebar.button("Refresh"):
    sid = st.session_state["session_id"]
    st.session_state.clear()
    st.session_state["session_id"] = sid








