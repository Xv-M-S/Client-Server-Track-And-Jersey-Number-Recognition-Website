from core.yolo_tracking.examples import track,track_new
from core.yolo_JNR.YoloJNR import infer_JNR
from core.yolo_JNR.id_to_num import id_to_num
from core.yolo_JNR.visual_JN import main_image,main_video
import cv2
import os,subprocess

def _preprocess(data):
    temp_data = {}
    # 遍历提交参数取值，处理上传的参数
    for k, v in data.items():
        if k == 'image':
            # 参数的默认值
            temp_data['user_id'] = data['user_id']
            temp_data['tracking_method'] = data['tracking_method'] if 'tracking_method' in data else "ocsort"
            temp_data['show_confidence'] = data['show_confidence'] if 'show_confidence' in data else "No"
            temp_data[k] = v
        elif k == 'video':
            # 参数的默认值
            temp_data['user_id'] = data['user_id']
            temp_data['tracking_method'] = data['tracking_method'] if 'tracking_method' in data else "ocsort"
            temp_data['show_confidence'] = data['show_confidence'] if 'show_confidence' in data else "No"
            temp_data[k] = v
        elif k == "Image_JNR":
            # 参数的默认值
            temp_data['user_id'] = data['user_id']
            temp_data['filter_confidence'] = float(data['filter_confidence']) if 'filter_confidence' in data else 0.7
            temp_data['recognition_confidence'] = float(data['recognition_confidence']) if 'recognition_confidence' in data else 0.7
            temp_data[k] = v
        elif k == "Video_JNR":
            # 参数的默认值
            temp_data['user_id'] = data['user_id']
            temp_data['filter_confidence'] = float(data['filter_confidence']) if 'filter_confidence' in data else 0.7
            temp_data['recognition_confidence'] = float(data['recognition_confidence']) if 'recognition_confidence' in data else 0.7
            temp_data[k] = v

    return temp_data

def _postprocess(data):
    current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
    current_folder_path = os.path.dirname(current_file_path)
    user_id = data["user_id"]
    if "image" in data:
        # 返回image上track的结果
        # 读取图像
        image_path = os.path.join(current_folder_path,"output",user_id,"image/detection_demo/demo.png")
        return image_path
    elif "Image_JNR" in data:
        # 返回image上JNR的结果
        # 读取图像
        image_path = os.path.join(current_folder_path,"output",user_id,"output.png")
        image = cv2.imread(image_path)
        return image_path
    elif "video" in data:
        # 返回video上track的结果
        # 读取输出视频文件的二进制数据
        video_path = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/demo.mp4")
        return video_path
    elif "Video_JNR" in data:
        # 返回video上JNR的结果
        # 读取输出视频文件的二进制数据
        video_path = os.path.join(current_folder_path,"output",user_id,"final_video.mp4")
        return video_path

    return False

def _inference(data):
    current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
    current_folder_path = os.path.dirname(current_file_path)
    user_id = data["user_id"]
    if "image" in data:
        # 执行image的tarck推理
        method =  data["tracking_method"]
        conf = True if data["show_confidence"] == "yes" else False
        if method == "ocsort":
            if conf:
                # 运行带置信度输出的代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--tracking-method", "ocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.png"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"image"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
            else:
                # 运行不带置信度的输出代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track_new.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--tracking-method", "ocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.png"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"image"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
                # os.system("mv ./results/image/detection_demo/video/output.mp4 ./results/image/detection_demo/demo.png")
        elif method == "strongsort":
            if conf:
                # 运行带置信度输出的代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--reid-model", "./core/yolo_tracking/pth/osnet_x1_0.pt",
                    "--tracking-method", "deepocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.png"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"image"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    # "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
            else:
                # 运行不带置信度的输出代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track_new.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--reid-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/osnet_x1_0.pt"),
                    "--tracking-method", "deepocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.png"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"image"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    # "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
    elif "video" in data:
        # 执行image的tarck推理
        method =  data["tracking_method"]
        conf = True if data["show_confidence"] == "True" else False
        if method == "ocsort":
            if conf:
                # 运行带置信度输出的代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--tracking-method", "ocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.mp4"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"video"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
            else:
                # 运行不带置信度的输出代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track_new.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--tracking-method", "ocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.mp4"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"video"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
                ori_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/final_video.mp4")
                des_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/demo.mp4")
                cmd = "mv " + ori_file + " " + des_file
                os.system(cmd)
        elif method == "strongsort":
            if conf:
                # 运行带置信度输出的代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--reid-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/osnet_x1_0.pt"),
                    "--tracking-method", "deepocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.mp4"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"video"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
            else:
                # 运行不带置信度的输出代码
                subprocess.run([
                    "python", os.path.join(current_folder_path,"core/yolo_tracking/examples/track_new.py"),
                    "--yolo-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/yolov8.pt"),
                    "--reid-model", os.path.join(current_folder_path,"core/yolo_tracking/pth/osnet_x1_0.pt"),
                    "--tracking-method", "deepocsort",
                    "--source", os.path.join(current_folder_path,"input",user_id,"demo.mp4"),
                    "--project", os.path.join(current_folder_path,"output",user_id,"video"),
                    "--name", "detection_demo",
                    "--save-id-crops",
                    "--classes", "0",
                    "--save", "--save-txt", "--save-mot",
                    "--device", "0"
                ])
                ori_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/final_video.mp4")
                des_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/demo.mp4")
                cmd = "mv " + ori_file + " " + des_file
                os.system(cmd)
        try:
            if conf:
                # 对于使用ocsort的方法，需要对视频进行格式的转换
                mp4_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/demo.mp4")
                # 视频格式转换
                from moviepy.editor import VideoFileClip
                avi_file = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/demo.avi")
                # 使用 VideoFileClip 加载 AVI 视频
                clip = VideoFileClip(avi_file)
                # 使用 write_videofile 将视频编码为 MP4 格式
                clip.write_videofile(mp4_file, codec="libx264")
        except Exception as e:
            print(f"Error loading video: {e}")
    elif "Image_JNR" in data:
        R_Conf = data["recognition_confidence"]
        F_Conf = data["filter_confidence"]
        data_path = os.path.join(current_folder_path,"output",user_id,"image/detection_demo/crops/0")
        infer_JNR(data_path,R_Conf,F_Conf,user_id)
        # num 替换 id 【已修改】
        motPath = os.path.join(current_folder_path,"output",user_id,"image/detection_demo/mot/"+ user_id +".txt")
        mappingFile=os.path.join(current_folder_path,'output',user_id,'id_num.txt')
        outFile=os.path.join(current_folder_path,'output',user_id,'mot.txt')
        id_to_num(mappingFile,motPath,outFile)
        print("run id_to_num success!")
        # 可视化
        main_image(os.path.join(current_folder_path,'input',user_id,'demo.png'), os.path.join(current_folder_path,'output',user_id,'mot.txt'),user_id)

    elif "Video_JNR" in data:
        R_Conf = data["recognition_confidence"]
        F_Conf = data["filter_confidence"]
        data_path = os.path.join(current_folder_path,"output",user_id,"video/detection_demo/crops/0")
        infer_JNR(data_path,R_Conf,F_Conf,user_id)

        # num 替换 id 【已修改】
        motPath = os.path.join(current_folder_path,"input",user_id,"demo.mp4.txt")
        mappingFile=os.path.join(current_folder_path,'output',user_id,'id_num.txt')
        outFile=os.path.join(current_folder_path,'output',user_id,'mot.txt')
        id_to_num(mappingFile,motPath,outFile)
        print("run id_to_num success!")
        # 可视化
        main_video(os.path.join(current_folder_path,'input',user_id,'demo.mp4'), os.path.join(current_folder_path,'output',user_id,'mot.txt'),user_id)
    return data
    

