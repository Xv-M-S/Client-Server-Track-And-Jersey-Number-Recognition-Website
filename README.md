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
conda activate track
pip install -r requirements.txt
pip install boxmot
pip3 install  --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple  Flask
pip install moviepy
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

