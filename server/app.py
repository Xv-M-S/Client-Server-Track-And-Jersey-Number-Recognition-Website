from flask import Flask, request , send_file
import json 
from service import _preprocess,_postprocess,_inference
import os
current_file_path = os.path.abspath(__file__) # 获取当前运行文件路径，并使用绝对路径
current_folder_path = os.path.dirname(current_file_path)
app = Flask(__name__)
DEBUG = 1
@app.route('/track_image', methods=['POST'])
def track_image_func():
    print("----------- in track_imag func ----------")
    data = {}
    data['user_id'] = request.form.get('user_id')
    data['image'] = request.form.get('image')
    data['tracking_method'] = request.form.get('tracking_method')
    data['show_confidence'] = request.form.get('show_confidence')

    # 创建相关专属文件夹
    if not os.path.exists(os.path.join(current_folder_path,"input",data['user_id'])):
        os.makedirs(os.path.join(current_folder_path,"input",data['user_id']))
    if not os.path.exists(os.path.join(current_folder_path,"output",data['user_id'])):
        os.makedirs(os.path.join(current_folder_path,"output",data['user_id']))
    else:
        os.system("rm -rf " + os.path.join(current_folder_path,"output",data['user_id']) + "/*")
    file = request.files['original_image']
    # 处理上传的文件
    if file:
        # 保存图片到指定位置
        save_path = os.path.join(current_folder_path,'input',data['user_id'],'demo.png')
        file.save(save_path)
        print('File uploaded:', file.filename)
    # 运行图片的track推理
    # 第一步，参数预处理
    if DEBUG:print(data)
    pre_data = _preprocess(data)
    if DEBUG:print(pre_data)
    # 第二步，运行推理代码
    pre_data = _inference(pre_data)
    # 第三步，后处理
    file_path = _postprocess(pre_data)
    if file_path == False:
        print("_postprocess wrong!!!")

    return send_file(file_path, mimetype='image/png')

@app.route('/track_video', methods=['POST'])
def track_video_func():
    print("----------- in track_video func ----------")
    data = {}
    data['user_id'] = request.form.get('user_id')
    data['video'] = request.form.get('video')
    data['tracking_method'] = request.form.get('tracking_method')
    data['show_confidence'] = request.form.get('show_confidence')

    # 创建相关专属文件夹
    if not os.path.exists(os.path.join(current_folder_path,"input",data['user_id'])):
        os.makedirs(os.path.join(current_folder_path,"input",data['user_id']))
    if not os.path.exists(os.path.join(current_folder_path,"output",data['user_id'])):
        os.makedirs(os.path.join(current_folder_path,"output",data['user_id']))
    else:
        os.system("rm -rf " + os.path.join(current_folder_path,"output",data['user_id']) + "/*")
    file = request.files['original_video']
    # 处理上传的文件
    if file:
        # 保存图片到指定位置
        save_path = os.path.join(current_folder_path,'input',data['user_id'],'demo.mp4')
        file.save(save_path)
        print('File uploaded:', file.filename)
    # 运行图片的track推理
    # 第一步，参数预处理
    if DEBUG:print(data)
    pre_data = _preprocess(data)
    if DEBUG:print(pre_data)
    # 第二步，运行推理代码
    pre_data = _inference(pre_data)
    # 第三步，后处理
    file_path = _postprocess(pre_data)
    if file_path == False:
        print("_postprocess wrong!!!")

    return send_file(file_path, mimetype='video/mp4')


@app.route('/JNR_image', methods=['POST'])
def JNR_image_func():
    print("----------- in JNR_image func ----------")
    # 读取数据
    data = {}
    data['user_id'] = request.form.get('user_id')
    data['Image_JNR'] = request.form.get('Image_JNR')
    data['filter_confidence'] = request.form.get('filter_confidence')
    data['recognition_confidence'] = request.form.get('recognition_confidence')

    # 处理数据
    # 运行图片的track推理
    # 第一步，参数预处理
    if DEBUG:print(data)
    pre_data = _preprocess(data)
    if DEBUG:print(pre_data)
    # 第二步，运行推理代码
    pre_data = _inference(pre_data)
    # 第三步，后处理
    file_path = _postprocess(pre_data)
    if file_path == False:
        print("_postprocess wrong!!!")

    return send_file(file_path, mimetype='image/png')

@app.route('/JNR_video', methods=['POST'])
def JNR_video_func():
    print("----------- in JNR_video func ----------")
    # 读取数据
    data = {}
    data['user_id'] = request.form.get('user_id')
    data['Video_JNR'] = request.form.get('Video_JNR')
    data['filter_confidence'] = request.form.get('filter_confidence')
    data['recognition_confidence'] = request.form.get('recognition_confidence')

    # 处理数据
    # 运行图片的track推理
    # 第一步，参数预处理
    if DEBUG:print(data)
    pre_data = _preprocess(data)
    if DEBUG:print(pre_data)
    # 第二步，运行推理代码
    pre_data = _inference(pre_data)
    # 第三步，后处理
    file_path = _postprocess(pre_data)
    if file_path == False:
        print("_postprocess wrong!!!")

    return send_file(file_path, mimetype='video/mp4')



# host must be "0.0.0.0", port must be 8080
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
