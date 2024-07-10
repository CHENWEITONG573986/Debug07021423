"""利用摄像头进行人脸识别.
"""

import os

import cv2
import numpy as np
import util.utils as u
from util.window_manager import WindowManager
from util.face_detector import FaceDetector
import codecs, json
from PIL import Image, ImageDraw, ImageFont
import multiprocessing
from multiprocessing import Process
from action.action import Controller
from collections import Counter
from ctypes import c_bool
from speech.speech import play

class Face:
    def __init__(self):
        """初始化.

        # 参数
            threshold: Float, threshold for specific face.
        """
        self._model = u.get_feature_model()
        self._windowManager = WindowManager('Face', self.on_keypress)
        self._faceDetector = FaceDetector()
        self.faces_data_path = './images/faces_data.json'
        self.faces_data_dic = json.loads(codecs.open(self.faces_data_path, 'r', encoding='utf-8').read())
        self.speak_flag = multiprocessing.Value(c_bool, False)
        self.action_flag = multiprocessing.Value(c_bool, False)
        self.recognition_name = ""
        self.recognition_index = ""
        self.r_cashe = []
        self.speak_process = None
        self.action_process = None
        self.ctrl = Controller()

    def run(self):
        """打开摄像头, 循环读取视频帧.
        """
        capture = cv2.VideoCapture(0)
        self._windowManager.create_window()
        while self._windowManager.is_window_created:

            success = capture.grab()
            _, frame = capture.retrieve()

            if frame is not None and success:
                faces = self._faceDetector.detect(frame)
                if self.faces_data_dic is not None and faces is not None:
                    labels = self._compare_distance(frame, faces)
                    frame = self._draw(frame, faces, labels)

                self._windowManager.show(frame)
                self._windowManager.process_events(frame, faces)

    def _get_feat(self, frame, face):
        """获取图像帧中的人脸特征.

        # Arguments
            frame: ndarray, 视频帧.
            face: tuple, 帧中的人脸坐标.

        # Returns
            feat: ndarray (128, ), 人脸特征.
        """
        f_h, f_w = frame.shape[:2]
        x, y, w, h = face
        x = max(0, x)
        y = max(0, y)
        w = min(f_w - x, w)
        h = min(f_h - y, h)
        img = frame[y: y + h, x: x + w, :]
        image = u.process_image(img)
        feat = self._model.predict(image)[0]

        return feat

    def _compare_distance(self, frame, faces):
        """计算视频帧中的人脸与已经录入的人脸数据集中的人脸的人脸特征之间的距离

        # Arguments
            frame: ndarray, 视频帧.
            faces: List, 帧中的人脸坐标.

        # Returns
            labels: list, 匹配到的人脸ID和人脸姓名以及人脸特征距离.
        """
        labels = []

        for (x, y, w, h) in faces:
            feat = self._get_feat(frame, (x, y, w, h))

            new_faces_data_dic = {}

            for faces_data_index, faces_data_value in self.faces_data_dic.items():
                face_name, face_feature = faces_data_value
                dist = np.linalg.norm(feat - np.array(face_feature))
                new_faces_data_dic.update({faces_data_index: (face_name, dist)})

            predict_face_index = min(new_faces_data_dic, key=lambda x : new_faces_data_dic[x][1])
            predict_face_name = new_faces_data_dic[predict_face_index][0]
            predict_face_dist = new_faces_data_dic[predict_face_index][1]
            print(predict_face_index, predict_face_name, predict_face_dist)
            labels.append((predict_face_index, predict_face_name, predict_face_dist))

        return labels

    def _draw(self, frame, faces, labels):
        """在图像帧中绘制矩形.

        # 参数
            frame: ndarray, 视频帧.
            faces: List, 帧中的人脸坐标.
            labels: List, 匹配到的人脸信息.

        # 返回
            f: ndarray, 绘制了矩形的帧.
        """
        f = frame.copy()
        color = [(0, 0, 255), (255, 0, 0)]
        if labels is None:
            label = [0 for _ in range(len(faces))]

        for rect, label in zip(faces, labels):
            (x, y, w, h) = rect
            cv2.rectangle(f, (x - 10, y - 10), (x + w + 10, y + h + 10), color[0], thickness=2)            
            dist = label[2]
            if dist < 1.5:

                predit_face_name = label[1]
                self.r_cashe.append(predit_face_name)
                if len(self.r_cashe) >= 10:
                    self.recognition_name = Counter(self.r_cashe).most_common(1)[0][0]
                    self.recognition_index = label[0]
                    self.r_cashe = []

                    if self.speak_process is None:
                        self.speak_process = Process(target=self.speak, args=(self.recognition_name, self.speak_flag))
                        print("speak_process start")
                        self.speak_process.run()
                        
                        print("欢迎你：", self.recognition_name)


                    if self.speak_flag.value:
                        if self.speak_process.is_alive():
                            self.speak_process.terminate()
                        if self.action_process is None:
                            self.action_process = Process(target=self.action, args=(self.action_flag, ))
                            print("action_process start")
                            self.action_process.run()
                            

                    if self.action_flag.value:
                        if self.action_process.is_alive():
                            self.action_process.terminate()                    
                        self.speak_process = None
                        self.action_process = None
                        self.speak_flag.value = False
                        self.action_flag.value = False
            else:
                self.recognition_name = "stranger"
            f = self.cv2ImgAddText(f, self.recognition_name, x + 30, x + 30, color[1], 20)
    
        flag = False
        return f

    def on_keypress(self, keycode, frame, faces):
        """处理按键事件.
        按esc键退出窗口.

        # 参数
            keycode: Integer, 按键, 27是ESC.
        """
        if keycode == 27:  # escape -> quit
            self._windowManager.destroy_window()




    def speak(self, text, speak_flag):
        print("i am speaking ")
        play(text)
        speak_flag.value = True
        print("i have speaked")
        

    def action(self, action_flag):
        print("i am acting")

        # self.ctrl.setMode()
        # self.ctrl.resetAngle()
        # self.ctrl.swing_arm()
        # self.ctrl.stretch_arm()
        # self.ctrl.bend_arm()
        action_flag.value = True
        print("i have acted")



    def cv2ImgAddText(self, img, text, left, top, textColor=(0, 255, 0), textSize=20):
        if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # 创建一个可以在给定图像上绘图的对象
        draw = ImageDraw.Draw(img)
        # 字体的格式
        fontStyle = ImageFont.truetype(
            "./font/simsun.ttc", textSize, encoding="utf-8")
        # 绘制文本
        draw.text((left, top), text, textColor, font=fontStyle)
        # 转换回OpenCV格式
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    face = Face()
    face.run()

