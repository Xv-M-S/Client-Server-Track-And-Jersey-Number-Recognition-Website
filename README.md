# ClientServer Track And JerseyNumberRecognition Website

This is a website code that implements football player tracking and player number identification.

# Quick Installtion Guide

**Clone the repositories**

```txt
git clone https://github.com/Xv-M-S/Client-Server-Track-And-Jersey-Number-Recognition-Website.git
```

**Server environment:**

```txt
conda create --name track_jnr python=3.10
conda activate track_jnr
pip install -r requirements.txt
pip install boxmot
pip3 install  --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple  Flask
pip install moviepy
pip install ultralytics
```

**Client environment:**

```txt
pip install streamlit
```

# Get started

**Run Server :**

```txt
cd server
python app.py
```

**Run Client :**

```txt
cd client
streamlit run client.py
```

## model

osnet
repo : https://github.com/MatthewAbugeja/osnet
model : https://kaiyangzhou.github.io/deep-person-reid/MODEL_ZOO.html

yolo_tracking 
repo : https://github.com/CV-Tracking/yolo_tracking

## debug

command:

``` bash
python core/yolo_tracking/examples/track.py \
  --yolo-model ./core/yolo_tracking/pth/yolov8.pt \
  --reid-model /home/sxm/flux-workspace/layout-to-image-zhuanlan/Client-Server-Track-And-Jersey-Number-Recognition-Website/server/core/yolo_tracking/pth/osnet_x1_0.pt \
  --tracking-method deepocsort \
  --source ./core/yolo_tracking/video/qiuxing01.mp4 \
  --project ./core/yolo_tracking/output \
  --name detection_demo \
  --save-id-crops \
  --save --save-txt --save-mot \
  --device 0
```
