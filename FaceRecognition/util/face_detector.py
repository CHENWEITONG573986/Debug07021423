"""Face detection model.
"""

import cv2
import numpy as np


class FaceDetector:
    def __init__(self):
        """Init.
        """
        self.detector = self._create_haar_detector()

    def _create_haar_detector(self):
        """创建haar级联分类器.

        # 参数
            path: String,分类器路径.

        # Returns
            face_cascade: harr分类器.
        """
        path = 'haarcascades/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(path)
        return face_cascade


    def detect(self, frame):
        """使用harr级联分类器检测人脸.

        # Arguments
            frame: ndarray(n, n, 3), 视频帧

        # Returns
            faces: List,视频帧中的人脸矩形框.
        """
        pic = frame.copy()
        gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5, minSize=(50, 50))
        # faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        return faces
