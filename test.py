# 导入up_controller模块中的UpController类
from up_controller import UpController
# 导入uptech模块
import uptech
# 导入time模块
import time
# 导入threading模块
import threading
# 导入cv2模块
import cv2
# 导入apriltag模块
import apriltag


# 创建一个UpTech对象
up = uptech.UpTech()
# 调用CDS_Open方法
up.CDS_Open()
# 调用LCD_Open方法，参数为2
up.LCD_Open(2)
# 调用ADC_IO_Open方法，获取open_flag
open_flag = up.ADC_IO_Open()
# 创建一个UpController对象
controller = UpController()

tag_id = -1
camera_id = 10
# 打开摄像头
cap = cv2.VideoCapture(camera_id)
# 创建AprilTag检测器
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))

# 设置摄像头分辨率
w = 640#640
h = 480#480
#     weight =320#320  #520
weight = 320
cap.set(3,w)
cap.set(4,h)

# 计算杯子的宽度和高度
cup_w = (int)((w - weight) / 2)
cup_h = (int)((h - weight) / 2) + 50   #   bian jie she zhi

while True:
    try:
        # 读取摄像头画面
        ret, frame = cap.read()
        frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
        camera_id = 0
        # 将画面转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测AprilTag
        tags = at_detector.detect(gray)
    
        # 获取第一个AprilTag的id
        tag_id = tags[0].tag_id if len(tags) else -1
#             cv2.imshow('video', frame)
        # 按键检测
        c = cv2.waitKey(1) & 0xff
        if c == 27:
            cap.release()
            break
    
    except Exception as e:
        print("Exception:", e)
        print(camera_id)
        # 在此处添加重新启动线程的代码
        cap.release()
        cap = cv2.VideoCapture(camera_id)
        camera_id = camera_id + 1
        if camera_id >2:
            camera_id = 0
        at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        continue
cap.release()
cv2.destroyAllWindows()