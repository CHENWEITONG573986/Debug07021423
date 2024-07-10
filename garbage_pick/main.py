from numpy.core.shape_base import block
from pigpio import LOW, NO_TX_WAVE
import cv2
import numpy as np
from controller import Controller
from multiprocessing import Process
from multiprocessing.managers import BaseManager


class ColorDetect:
    def __init__(self):
        self.target_H = 0
        self.target_S = 0
        self.target_V = 0
        self.gray_frame = None
        self.hsv_frame = None
        self.target_x = None
        self.target_y = None
        self.block = False
        self.hold_list = {"green": (160, 180, 100, 255, 100, 255), "yellow": (20, 40, 100, 255, 100, 255)}
        self.hold_list = {"green": (50, 77, 100, 255, 46, 255), "yellow": (20, 40, 100, 255, 100, 255)}
      
        self.cnts_list = []
        self.cnt = None
        self.color = None

        BaseManager.register('Controller', Controller)
        manager = BaseManager()
        manager.start()
        self.up = manager.Controller()
        controller_up = Process(name="controller_up", target=self.controller_init)
        controller_up.start()

    def controller_init(self):
        """初始化舵机
        进行相关初始化舵机的设置
        :return: 无
        """
        print("process start")
        self.up.lcd_display("ball_pick")
        motor_ids = [1,2,3,4]
        servo_ids = [5,6,7,8,9]
        self.up.set_cds_mode(motor_ids,1)
        self.up.set_cds_mode(servo_ids,0)
    


    def update_frame(self, frame):
        """检测指定阈值的色块.
        此函数用于将指定阈值的色块用矩形框框出来.
        检测多个颜色的多个色块.
        将多个色块与轮式机器人的距离按照距离远近进行排序.
        :param frame: ndarray, 视频帧.
        :return: 无.
        """
        c_list = [] 
        for color, hold in self.hold_list.items():
            h_min, h_max, s_min, s_max, v_min, v_max = hold       
            self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            low_color = np.array([h_min, s_min, v_min])
            high_color = np.array([h_max, s_max, v_max])
            mask = cv2.inRange(self.hsv_frame, low_color, high_color)  
            mask = cv2.medianBlur(mask, 7)
            cv2.imshow("mask", mask)
            cnts, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   
            if cnts != None:
                if self.block is False:
                    global cnt
                    for cnt in cnts:
                        (x, y, w, h) = cv2.boundingRect(cnt)
                        if w<30 or h<30:
                            continue
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  
                        font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
                        cv2.putText(frame, 'target', (x, y - 5), font, 0.7, (0, 0, 255), 2)
                        target_y = y+h/2
                        c_list.append((target_y, cnt, color))        
        self.cnts_list = sort(c_list)


    
    def pick(self):
        """捡取垃圾
        从检测到的色块列表里, 取出最近的色块作为抓取对象.
        通过前后左右移动不断调整轮式机器人与色块的距离, 移动过程中可以调节轮式机器人速度, 距离近了减速.
        轮式机器人到达合适位置后, 开始执行抓取动作, 根据不同的颜色执行不同的抓取动作.
        :return: 无
        """       
        if self.block is False:
            if len(self.cnts_list) != 0:
                _, self.cnt, self.color = self.cnts_list[0] # 每次都抓取距离最近的那一个
                (x, y, w, h) = cv2.boundingRect(self.cnt)
                self.target_x = x+w/2
                self.target_y = y+h/2
                print(self.target_x, self.target_y)
                if self.target_y > 350 and self.target_x > 150 and self.target_x < 290 :
                    self.up.set_controller_cmd(Controller.SPEED_DOWN)
                # else:
                #     self.up.set_controller_cmd(Controller.SPEED_UP)
                if self.target_y < 380:
                    self.up.set_controller_cmd(Controller.MOVE_FORWARD)
                elif self.target_y > 420:
                    self.up.set_controller_cmd(Controller.MOVE_BACKWARD)      
                elif self.target_x < 210:
                    self.up.set_controller_cmd(Controller.MOVE_LEFT)
                elif self.target_x > 250:
                    self.up.set_controller_cmd(Controller.MOVE_RIGHT)               
                else:
                    self.block = True          
                    if self.color == "yellow":
                        self.up.set_controller_cmd(Controller.PICK_UP_YELLOW)
                    elif self.color == "green":
                        self.up.set_controller_cmd(Controller.PICK_UP_GREEN)
        
        if self.up.get_controller_cmd() == Controller.NO_CONTROLLER:
            self.block = False
        
def sort(alist):
    """冒泡排序
    将传进来的色块列表按照色块跟轮式机器人的距离(int)的排序.
    :param alist: list 色块列表, 单个元素是由 色块跟轮式机器人的距离(int), 图像轮廓(ndarray), 色块颜色三个数据组成的元组.
    :return alist: list 返回排完序的列表
    """
    n = len(alist)
    for j in range(n-1):
        count = 0
        for i in range(0, n-1-j):
            if alist[i][0] < alist[i+1][0]:
                alist[i],alist[i+1] = alist[i+1],alist[i]
                count +=1
        if 0 == count:
            break
    return alist

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cd = ColorDetect()
    if cap.isOpened() is True:  # 检查摄像头是否正常启动
        while True:
            ret, frame = cap.read()
            cd.update_frame(frame)
            cd.pick()
            cv2.imshow("img", frame)
            if cv2.waitKey(30) & 0xff == ord('q'):
                break
        ctrl = Controller()
        ctrl.move_stop()
        cap.release()
        cv2.destroyAllWindows()
    
