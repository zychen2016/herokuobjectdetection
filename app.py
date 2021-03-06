from ObjectDetector import Detector
import io
import os
from flask import Flask, render_template, request

from PIL import Image
from flask import send_file
import time
from urllib.parse import unquote
def get_dataDict(data):
    data_dict={}
    for text in data.split("&"):
        key,value=text.split("=")
        value_1=unquote(value)
        data_dict[key]=value_1
    return data_dict


app = Flask(__name__)

detector = Detector()

# detector.detectNumberPlate('twocar.jpg')

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def upload():
    if request.method == 'POST':
        startTime=time.time()
        received_file = request.files['file']
        imageFileName = received_file.filename
        if received_file:
            # 保存接收的图片到指定文件夹
            received_dirPath = './resources/received_images'
            if not os.path.isdir(received_dirPath):
                os.makedirs(received_dirPath)
            imageFilePath = os.path.join(received_dirPath, imageFileName)
            received_file.save(imageFilePath)
            print('接收图片文件保存到此路径：%s' % imageFilePath)
            usedTime = time.time() - startTime
            print('接收图片并保存，总共耗时%.2f秒' % usedTime)
            image = Image.open(imageFilePath)
            #file = Image.open(request.files['file'].stream)
            start=time.time()
            img = detector.detectObject(image)
            end=time.time()
            print("time for saving is %s"%str(end-start))
            return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')

if __name__ == "__main__":
    app.run()
