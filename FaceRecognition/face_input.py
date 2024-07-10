"""验证模型, 人脸数据录入
"""

import os
import cv2
from util import utils as u
from util.window_manager import WindowManager
from util.face_detector import FaceDetector
import codecs, json


class Face:
    def __init__(self, face_index, face_name):
        """初始化

        # 参数
            face_index: Integer, 人脸的ID.
            face_name: String, 人脸姓名.
        """
        self._face_index = face_index
        self._face_name = face_name
        self._faces_data_path = './images/faces_data.json'
        self._faces_data_dic = self._load_faces_data()
        self._model = u.get_feature_model()
        self._windowManager = WindowManager('Face', self.on_keypress)
        self._faceDetector = FaceDetector()

    def run(self):
        """打开摄像头, 循环读取帧.
        """
        capture = cv2.VideoCapture(0)

        self._windowManager.create_window()
        while self._windowManager.is_window_created:

            success = capture.grab()
            _, frame = capture.retrieve()

            if frame is not None and success:
                faces = self._faceDetector.detect(frame)
                if len(faces) > 0:
                    frame = self._draw(frame, faces)

                self._windowManager.show(frame)
                self._windowManager.process_events(frame, faces)

    def _load_faces_data(self):
        """加载已录入的人脸数据.
        """


        if os.path.exists(self._faces_data_path):
            faces_data = json.loads(codecs.open(self._faces_data_path, 'r', encoding='utf-8').read())
        else:
            faces_data = {}

        return faces_data

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
        # 将当前帧保存为图片
        img_path = './images/person' 
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        img_name = '%s.jpg' %(self._face_index)        
        cv2.imwrite(os.path.join(img_path, img_name), img)
        image = u.process_image(img)
        feat = self._model.predict(image)[0]

        return feat


    def _draw(self, frame, faces):
        """在图像帧中绘制矩形.

        # 参数
            frame: ndarray, 视频帧.
            faces: List, 帧中的人脸坐标.

        # 返回
            f: ndarray, 绘制了矩形的帧.
        """
        f = frame.copy()
        color = [(0, 0, 255), (255, 0, 0)]

        for rect in faces:
            x, y, w, h = rect
            f = cv2.rectangle(f, (x, y),
                              (x + w, y + h),
                              color[0], 2)

        return f

    def on_keypress(self, keycode, frame, faces):
        """处理按键事件.
        按esc键退出窗口.
        按空格键录制脸部.

        # 参数
            keycode: Integer, 按键, 32是空格, 27是ESC.
            frame: ndarray, 视频帧.
            faces: List, 帧中的人脸坐标
        """
        if keycode == 32:  # space -> save face.
            faces_num = len(faces)
            if faces_num == 0:
                print("未检测到人脸，请正对摄像头！")
            elif faces_num > 1:
                print("检测到多张人脸，请无关人员离开！")
            else:
                feat = self._get_feat(frame, faces[0])
                self._faces_data_dic.update({str(self._face_index):(self._face_name, feat.tolist())})
                json.dump(self._faces_data_dic, open(self._faces_data_path, "w", encoding="utf-8"), separators=(',', ':'), sort_keys=True, indent=4)
                print('人脸已录入，按空格重新录入，或者按esc退出！')
        elif keycode == 27:  # escape -> quit
            self._windowManager.destroy_window()


if __name__ == '__main__':
    face_index = input("请输入你的员工编号：")
    face_name = input("请输入你的名字：")
    face = Face(face_index, face_name)
    face.run()

