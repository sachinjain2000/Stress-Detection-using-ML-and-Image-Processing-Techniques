from django.conf import settings
from PyEmotion import *
import cv2 as cv
class ImageExpressionDetect:
    def getExpression(self,imagepath):
        filepath = settings.MEDIA_ROOT + "\\" + imagepath
        PyEmotion()
        er = DetectFace(device='cpu', gpu_id=0)
        # Open you default camera
        # img = cv.imread('test.jpg')
        # cap = cv.VideoCapture(0)
        # ret, frame = cap.read()
        frame, emotion = er.predict_emotion(cv.imread(filepath))
        cv.imshow('Alex Corporation', frame)
        cv.waitKey(0)
        print("Hola Hi",filepath,"Emotion is ",emotion)
        return emotion

    def getLiveDetect(self):
        print("Streaming Started")
        PyEmotion()
        er = DetectFace(device='cpu', gpu_id=0)
        # Open you default camera
        cap = cv.VideoCapture(0)
        while (True):
            ret, frame = cap.read()
            frame, emotion = er.predict_emotion(frame)
            cv.imshow('Press Q to Exit', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()
