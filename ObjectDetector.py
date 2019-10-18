import cv2 as cv
import numpy


classNames = {0:'background',
              1:'bak',
              2:'black',
              3:'blackpearl',
              4:'gold',
              5:'redrose',
              6:'sunrose',
              7:'xiangyu',
              8:'chixiazhu',
              9:'hongti',
              10:'meirenzhi',
              11:'redball'
              }


class Detector:
    def __init__(self):
        global cvNet
        cvNet = cv.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                             'models/tf_graph.pbtxt')

    def detectObject(self, imName):
        img = cv.cvtColor(numpy.array(imName), cv.COLOR_BGR2RGB)
        cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
        detections = cvNet.forward()
        cols = img.shape[1]
        rows = img.shape[0]

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])

                xLeftBottom = int(detections[0, 0, i, 3] * cols)
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop = int(detections[0, 0, i, 5] * cols)
                yRightTop = int(detections[0, 0, i, 6] * rows)

                cv.rectangle(img, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                             (0, 0, 255))
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv.putText(img, label, (xLeftBottom+5, yLeftBottom), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        img = cv.imencode('.jpg', img)[1].tobytes()
        return img
