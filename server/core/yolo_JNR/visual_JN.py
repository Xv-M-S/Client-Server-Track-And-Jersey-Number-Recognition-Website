import cv2
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import ImageSequenceClip
import os
# 读取MOT16格式的追踪数据
def read_mot16(filename):
    tracks = {}
    with open(filename, 'r') as file:
        for line in file:
            data = line.split()
            frame, track_id, x, y, w, h = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])
            if frame not in tracks:
                tracks[frame] = []
            tracks[frame].append((track_id, x, y, w, h))
    return tracks


colors = {}

# 绘制边界框和ID
def draw_boxes(frame, boxes):
    for box in boxes:
        track_id, x, y, w, h = box
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        if track_id not in colors:
            # 为新的 track_id 生成一个随机颜色
            colors[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.rectangle(frame, top_left, bottom_right, colors[track_id], 3)
        if track_id > 0:
            cv2.putText(frame, str(track_id), (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1.2, colors[track_id], 2)

# 视频处理主程序
def main_video(video_path, mot16_path, user_id):
    current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
    current_folder_path = os.path.dirname(current_file_path)
    # 读取追踪数据
    tracks = read_mot16(mot16_path)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # 获取视频属性
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 创建视频写入器
    # 创建视频写入器对象
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4v编解码器
    # fps = 25  # 帧率为30
    # out = cv2.VideoWriter('./output/output.mp4', fourcc, fps, (frame_width, frame_height))
    out = cv2.VideoWriter(os.path.join(current_folder_path,'../../output',user_id,'output.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # 处理视频的每一帧
    frame_id = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 如果当前帧有追踪数据，则绘制边界框和ID
        if frame_id in tracks:
            draw_boxes(frame, tracks[frame_id])

        # 写入输出视频
        out.write(frame)
        frame_id += 1

    # 释放资源
    cap.release()
    out.release()

    # 添加声音
    video = VideoFileClip(video_path)
    # 获取视频的音频-不加音频steamlit显示不出来
    audio = video.audio
    output_video = os.path.join(current_folder_path,"../../output",user_id,"output.mp4")
    final_video = concatenate_videoclips([VideoFileClip(output_video)])
    final_video = final_video.set_audio(audio)
    final_path = os.path.join(current_folder_path,"../../output",user_id,"final_video.mp4")
    final_video.write_videofile(final_path)
    # os.remove(output_video)

# 图像处理主程序
def main_image(image_path, mot16_path,user_id):
    current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
    current_folder_path = os.path.dirname(current_file_path)
    # 读取追踪数据
    tracks = read_mot16(mot16_path)

    # 读取图像文件
    image = cv2.imread(image_path)

    # 获取视频属性
    height, width = image.shape[:2]
    
    frame_id = 1
    # 如果当前帧有追踪数据，则绘制边界框和ID
    if frame_id in tracks:
        draw_boxes(image, tracks[frame_id])
    # 输出图片
    cv2.imwrite(os.path.join(current_folder_path,"../../output",user_id,"output.png"), image)


# 运行主程序
# main_vedio('/home/sxm/YoloTracking/YOLOv8-streamlit-app/input/demo.mp4', './results/JNR/mot.txt')
# main_image('/home/sxm/YoloTracking/YOLOv8-streamlit-app/input/demo.png', './results/JNR/mot.txt')