# Mikel Broström 🔥 Yolo Tracking 🧾 AGPL-3.0 license

import numpy as np
import torch
from ultralytics.utils import ops
import random,cv2,os


def write_mot_results(txt_path, results, frame_idx):
    nr_dets = len(results.boxes)
    frame_idx = torch.full((1, 1), frame_idx + 1)
    frame_idx = frame_idx.repeat(nr_dets, 1)
    dont_care = torch.full((nr_dets, 1), -1)
    mot = torch.cat([
        frame_idx,
        results.boxes.id.unsqueeze(1).to('cpu'),
        ops.xyxy2ltwh(results.boxes.xyxy).to('cpu'),
        results.boxes.conf.unsqueeze(1).to('cpu'),
        results.boxes.cls.unsqueeze(1).to('cpu'),
        dont_care
    ], dim=1)

    # create parent folder
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    # create mot txt file
    txt_path.touch(exist_ok=True)

    with open(str(txt_path), 'ab+') as f:  # append binary mode
        np.savetxt(f, mot.numpy(), fmt='%d')  # save as ints instead of scientific notation


colors = {}

def get_color(track_id):
    if track_id not in colors:
        # 为新的 track_id 生成一个随机颜色
        colors[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return colors[track_id]

def video_mot_results(frame_id, results, path, video_writer=None):
    image = results.orig_img.copy()
    nr_dets = len(results.boxes)
    # print("Visualization results saved ")

    if results.boxes.data.shape[1] == 7:
    # 遍历每个检测结果
        # for i in range(nr_dets):
        #     track_id = int(results.boxes.id[i].item())
        #     if results.boxes.data.shape[1] == 7:
        #         bbox = results.boxes.xyxy[i]

        #         # 在图像上绘制边界框和轨迹ID
        #         cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 255), 3)
        #         cv2.putText(image, str(track_id), (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 2)
        for i in range(nr_dets):
            track_id = int(results.boxes.id[i].item())
            if results.boxes.data.shape[1] == 7:
                bbox = results.boxes.xyxy[i]

                # 获取 track_id 对应的颜色
                color = get_color(track_id)

                # 在图像上绘制边界框和轨迹ID
                cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 5)
                cv2.putText(image, str(track_id), (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_COMPLEX, 1.5, color, 3)

    # 保存渲染后的图像
    os.makedirs(path, exist_ok=True)
    save_path = os.path.join(path, "output.mp4")

    if video_writer is None:
        # 创建视频写入器对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4v编解码器
        fps = 25  # 帧率为30
        video_writer = cv2.VideoWriter(save_path, fourcc, fps, (image.shape[1], image.shape[0]))

    # 写入图像帧到视频文件
    video_writer.write(image)

    return video_writer