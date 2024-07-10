import cv2
import numpy as np
import utils
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

font = cv2.FONT_HERSHEY_SIMPLEX

class ColorDetect:
    def __init__(self):
        self.target_H = 0
        self.target_S = 0
        self.target_V = 0
        self.gray_frame = None
        self.hsv_frame = None
        self.target_x = None
        self.target_y = None

    
    def mouse_click(self, event, x, y, flags, para):
        """通过鼠标调整滑动条的数值
        此函数用于通过调整滑动条的数值来检测色块的颜色阈值
        :param event: 鼠标点击事件, 例如点击左键.
        :param x: int 像素点坐标
        :param y: int 像素点坐标
        :param flags: int
        :param params: NoneType
        :return:
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            print ('PIX: ', x, y)
            print ('GRAY: ', self.gray_frame[y, x])
            print ('HSV: ', self.hsv_frame[y, x])

    
    def update_frame(self, img, h_min, h_max, s_min, s_max, v_min, v_max):
        """检测指定阈值的色块
        此函数用于将指定阈值的色块用矩形框框出来

        :param img:  ndarray, 视频帧.
        :param h_min: int, 色调最小值
        :param h_max: int, 色调最大值
        :param s_min: int, 饱和度最小值
        :param s_max: int, 饱和度最大值
        :param v_min: int, 明度最小值
        :param v_max: int, 明度最大值
        :return: 无
        """
        src_frame = img
        result = src_frame
        self.gray_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2GRAY)
        self.hsv_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2HSV)
        low_color = np.array([h_min, s_min, v_min])
        high_color = np.array([h_max, s_max, v_max])
        mask_color = cv2.inRange(self.hsv_frame, low_color, high_color)
        mask_color = cv2.medianBlur(mask_color, 7)
        cv2.imshow("mask", mask_color)
        cnts, hierarchy = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in cnts:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)  
            cv2.putText(result, 'target', (x, y - 5), font, 0.7, (0, 0, 255), 2)


            
     
def nothing(x):
    pass


if __name__ == '__main__':
    """检测颜色方块的阈值
    运行该方法后, 窗口会出现三个可以调整数值的滑动条, 分别对应: 色调（H）, 饱和度（S）, 明度（V）.
    同时还会出现一个显示窗口, 通过显示窗口, 可以看到摄像头拍摄到的内容.
    通过调整滑动条的数值, 当颜色方块被出现的蓝色框线框起来时, 我们就获取到了颜色方块的阈值.
    """
    cap = cv2.VideoCapture(0)
    cd = ColorDetect()
    cv2.namedWindow('img')
    cv2.createTrackbar("H_MIN","img",35,180,nothing)
    cv2.createTrackbar("H_MAX","img",40,180,nothing)
    cv2.createTrackbar("S_MIN","img",100,255,nothing)
    cv2.createTrackbar("S_MAX","img",115,255,nothing)
    cv2.createTrackbar("V_MIN","img",180,255,nothing)
    cv2.createTrackbar("V_MAX","img",190,255,nothing)
    cv2.setMouseCallback("img", cd.mouse_click)

    while True:
        ret, frame = cap.read()
        r_Img = frame
        r_Img = cv2.rotate(frame, cv2.ROTATE_180)
        h_min = cv2.getTrackbarPos("H_MIN","img")
        h_max = cv2.getTrackbarPos("H_MAX","img")
        s_min = cv2.getTrackbarPos("S_MIN","img")
        s_max = cv2.getTrackbarPos("S_MAX","img") 
        v_min = cv2.getTrackbarPos("V_MIN","img")
        v_max = cv2.getTrackbarPos("V_MAX","img")
        cd.update_frame(r_Img, h_min, h_max, s_min, s_max, v_min, v_max)
        cv2.imshow("img", r_Img)
        if cv2.waitKey(30) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()