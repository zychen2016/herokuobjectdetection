from ObjectDetector import Detector
import io

from flask import Flask, render_template, request

from PIL import Image
from flask import send_file
import time
from urlib.parse import unquote
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
        start=time.time()
        #file = Image.open(request.files['file'].stream)
        data_bytes=request.get_data()
        data = data_bytes.decode('utf-8')
        data_dict = get_dataDict(data)
        if 'image_base64_string' in data_dict:
            # 保存接收的图片到指定文件夹
            received_dirPath = '../resources/received_images'
            if not os.path.isdir(received_dirPath):
                os.makedirs(received_dirPath)
            timeString = get_timeString()
            imageFileName = timeString + '.jpg'
            imageFilePath = os.path.join(received_dirPath, imageFileName)
            try:
                image_base64_string = data_dict['image_base64_string']
                image_base64_bytes = image_base64_string.encode('utf-8')
                image_bytes = base64.b64decode(image_base64_bytes)
                with open(imageFilePath, 'wb') as file:
                    file.write(image_bytes)
                print('接收图片文件保存到此路径：%s' %imageFilePath)
                usedTime = time.time() - startTime
                print('接收图片并保存，总共耗时%.5f秒' %usedTime)
                # 通过图片路径读取图像数据，并对图像数据做目标检测
                startTime = time.time()
                image = Image.open(imageFilePath)
                img = detector.detectObject(image)
                print("time for saving is %s"%str(end-start))
                return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')
            except Exception as e:
                print(e)
if __name__ == "__main__":
    app.run()
