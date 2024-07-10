import threading
from typing import Tuple
from up_controller import UpController
import time
import cv2
import apriltag
import sys
import numpy as np




class MatchDemo:

    FD = 150
    RD = 150
    BD = 150
    LD = 180

    # 倾斜计时
    na = 0
    # 推箱子计时
    nb = 0
    # 旋转计时
    nc = 8
    # 前搁浅计时
    nd = 0
    # 后搁浅计时
    ne = 8
    # 倾斜
    qx = 0

    def __init__(self):
        self.version = "1.0"
        self.servo_speed = 800
        self.controller = UpController()
        self.controller.lcd_display("MatchDemo")
        # 设置
        self.controller.set_chassis_mode(2)
        motor_ids = [1, 2]
        servo_ids = [5, 6, 7, 8]
        self.controller.set_cds_mode(motor_ids, 1)
        self.controller.set_cds_mode(servo_ids, 0)
        
        self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        self.apriltag_width = 0
        self.tag_id = -1
        apriltag_detect = threading.Thread(target = self.apriltag_detect_thread)
        apriltag_detect.setDaemon(True)
        apriltag_detect.start()
        

    def apriltag_detect_thread(self):
        print("detect start")
        cap = cv2.VideoCapture(0)

        w = 640
        h = 480
        weight = 320
        cap.set(3,w)
        cap.set(4,h)

        cup_w = (int)((w - weight) / 2)
        cup_h = (int)((h - weight) / 2) + 50

        while True:
            ret, frame = cap.read()
            frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tags = self.at_detector.detect(gray)
            for tag in tags:
                self.tag_id = tag.tag_id
                print("tag_id = {}".format(tag.tag_id))
                cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
                cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
                cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
                cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
            cv2.imshow("img", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    # 默认上台动作
    def default_platform(self):
        self.controller.up.CDS_SetAngle(5, 424, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 424, self.servo_speed)

    # 收前爪
    def pack_up_ahead(self):
        self.controller.up.CDS_SetAngle(5, 900, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 124, self.servo_speed)
        time.sleep(0.01)
        self.controller.up.CDS_SetAngle(5, 900, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 124, self.servo_speed)

    # 收后爪
    def pack_up_behind(self):
        self.controller.up.CDS_SetAngle(7, 124, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 900, self.servo_speed)
        time.sleep(0.01)
        self.controller.up.CDS_SetAngle(7, 124, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 900, self.servo_speed)


    # 上台后爪子的状态
    def shovel_state(self):
        self.controller.up.CDS_SetAngle(5, 780, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 244, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 244, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 780, self.servo_speed)

    # 前上台动作
    def go_up_ahead_platform(self):
        self.controller.move_cmd(0, 0)
        time.sleep(0.1)
        # 爪子抬起
        self.default_platform()
        time.sleep(0.4)
        self.controller.move_cmd(500, 500)
        time.sleep(0.7)
        # 支前爪
        self.pack_up_ahead()
        time.sleep(0.8)
        # 收起前爪
        self.controller.up.CDS_SetAngle(5, 424, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 600, self.servo_speed)
        # 支后爪
        time.sleep(0.5)
        self.pack_up_behind()
        time.sleep(0.8)
        # 默认上台
        self.controller.up.CDS_SetAngle(7, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 424, self.servo_speed)
        # self.default_platform()
        time.sleep(1)
        self.controller.move_cmd(0, 0)
        time.sleep(0.5)

    # 后上台
    def go_up_behind_platform(self):
        self.controller.move_cmd(0, 0)
        time.sleep(0.1)
        # 爪子抬起
        self.default_platform()
        time.sleep(0.4)
        self.controller.move_cmd(-500, -500)
        time.sleep(0.6)
        # 支前爪
        self.pack_up_behind()
        time.sleep(0.9)
        # 收起前爪
        self.controller.up.CDS_SetAngle(7, 640, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 384, self.servo_speed)
        # 支后爪
        time.sleep(0.5)
        self.pack_up_ahead()
        time.sleep(0.8)
        # 默认上台
        self.default_platform()
        time.sleep(1)
        self.controller.move_cmd(0, 0)
        time.sleep(0.5)

    # 检测是否在台上-返回状态
    def paltform_detect(self):
        angle_sensor = self.controller.adc_data[0]
        ahead_ad = 1 if self.controller.adc_data[1] < 1000 else 0
        right_ad = 1 if self.controller.adc_data[2] < 1000 else 0
        behind_ad = 1 if self.controller.adc_data[3] < 1000 else 0
        left_ad = 1 if self.controller.adc_data[4] < 1000 else 0
        sum = ahead_ad + right_ad + behind_ad + left_ad
        if angle_sensor > 1500 and angle_sensor < 3000:
            if sum >= 2:
                # 在台下
                return 0
            else:
                # 在台上
                return 1
        elif angle_sensor <= 1500:
            # 卡在擂台左侧在地面右侧在擂台
            return 3
        else:
            # 卡在擂台右侧在地面左侧在擂台
            return 4

    def fence_detect(self):
        # 底部前方红外光电
        ad1 = self.controller.adc_data[1]
        # 底部右侧红外光电
        ad2 = self.controller.adc_data[2]
        # 底部后方红外光电
        ad3 = self.controller.adc_data[3]
        # 底部左侧红外光电
        ad4 = self.controller.adc_data[4]

        # 前红外测距传感器
        ad5 = self.controller.adc_data[5]
        # 右红外测距传感器
        ad6 = self.controller.adc_data[6]
        # 后红外测距传感器
        ad7 = self.controller.adc_data[7]
        # 左红外测距传感器
        ad8 = self.controller.adc_data[8]


        # ----------------------对擂台，一个测距检测到--------------------
        if ad3 < 1000 and ad2 > 1000 and ad4 > 1000 and ad5 > self.FD and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，后方对擂台
            return 1
        if ad4 < 1000 and ad1 > 1000 and ad3 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，左侧对擂台
            return 2
        if ad1 < 1000 and ad2 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方对擂台
            return 3
        if ad2 < 1000 and ad1 > 1000 and ad3 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，右侧对擂台
            return 4

        # ------------------------对围栏，两个相邻测距检测到-------------
        if ad2 > 1000 and ad3 > 1000 and ad5 > self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，前左检测到围栏
            return 5

        if ad3 > 1000 and ad4 > 1000 and ad5 > self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，前右检测到围栏
            return 6
        if ad1 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，后右检测到围栏
            return 7
        if ad1 > 1000 and ad2 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，后左检测到围栏
            return 8

        # --------------------------台上有敌人，两个相对测距检测到-----------
        if ad5 > self.FD and ad6 < self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方或后方有台上敌人
            return 9
        if ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，左侧或右侧由台上敌人
            return 10

        # -------------------------三侧有障碍，三个测距检测到---------------
        if ad5 > self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，前方、左侧和右侧检测到围栏
            return 11
        if ad5 > self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方、右侧和后方检测到围栏
            return 12
        if ad5 > self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，前方、左侧和后方检测到围栏
            return 13
        if ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，右侧、左侧和后方检测到围栏
            return 14

        # -----------------------斜对擂台，两个红外光电检测到----------------
        if ad1 < 1000 and ad2 < 1000 and ad5 < self.FD and ad6 < self.RD:
            # 在台下，前方和右侧对擂台其他传感器没检测到
            return 15
        if ad1 < 1000 and ad4 < 1000 and ad5 < self.FD and ad8 < self.LD:
            # 在台下，在台下，前方和左侧对擂台其他传感器没检测到
            return 16
        if ad2 < 1000 and ad3 < 1000 and ad6 < self.FD and ad7 < self.RD:
            # 在台下，后方和右侧对擂台其他传感器没检测到
            return 17
        if ad3 < 1000 and ad4 < 1000 and ad7 < self.FD and ad8 < self.LD:
            # 在台下，后方和左侧对擂台其他传感器没检测到
            return 18
        else:
            return 101


    def edge_detect(self):
        # 左前红外光电传感器
        io_0 = self.controller.io_data[0]
        # 右前红外光电传感器
        io_1 = self.controller.io_data[1]
        # 右后红外光电传感器
        io_2 = self.controller.io_data[2]
        # 左后红外光电传感器
        io_3 = self.controller.io_data[3]
        # 获取前方测距值
        ad5 = self.controller.adc_data[5]
        # 获取后方测距值
        ad7 = self.controller.adc_data[7]

        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # 没有检测到边缘
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # 左前检测到边缘
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            # 右前检测到边缘
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            # 右后检测到边缘
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # 左后检测到边缘
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            # 前方两个检测到边缘
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            # 后方两个检测到边缘
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # 左侧两个检测到边缘
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            # 右侧两个检测到边缘
            return 8
        elif io_0 == 1 and io_1 == 1 and io_2 == 1 and io_3 == 1 and ad5 > 480:
            # 搁浅放在擂台下
            return 9
        elif io_0 == 1 and io_1 == 1 and io_2 == 1 and io_3 == 1 and ad7 > 480:
            # 搁浅放在擂台上
            return 10
        else:
            return 102

    # 敌人检测
    def enemy_detect(self):
        # 底部前方红外光电
        ad1 = self.controller.adc_data[1]
        # 底部右侧红外光电
        ad2 = self.controller.adc_data[2]
        # 底部后方红外光电
        ad3 = self.controller.adc_data[3]
        # 底部左侧红外光电
        ad4 = self.controller.adc_data[4]
        # 前红外测距传感器
        ad5 = self.controller.adc_data[5]

        #print("ad1 = {} , ad2 = {} , ad3 = {}, ad4 = {} , ad5 = {}".format(ad1,ad2,ad3,ad4,ad5))

        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:
            # 无敌人
            return 0
        if ad1 < 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:

            
            if ad5 > 1000:
                # 前方是箱子
                return 11
            else:
                # 前方有敌人
                if self.tag_id != 2 or self.tag_id == -1:
                    # 前方是敌人
                    return 1
                else:
                
                    return 5
        if ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 > 100:
            # 右侧有敌人或棋子
            return 2
        if ad1 > 100 and ad2 > 100 and ad3 < 100 and ad4 > 100:
            # 后方有敌人或棋子
            return 3
        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 < 100:
            # //左侧有敌人或棋子
            return 4
        else:
            return 103



    def start_match(self):
        self.default_platform()
        time.sleep(1)
        # self.go_up_ahead_platform()
        while 1:
            stage = self.paltform_detect()
            time.sleep(0.01)
            # print(stage)
            # 在台下
            if stage == 0:
                fence = self.fence_detect()
                # 在台下后方对擂台
                if fence == 1:
                    self.go_up_behind_platform()
                # 左侧对擂台
                if fence == 2:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(-400, 400)
                            time.sleep(0.002)
                # 前方对擂台
                if fence == 3:
                    self.go_up_ahead_platform()
                # 右侧对擂台
                if fence == 4:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(400, -400)
                            time.sleep(0.02)
                # 前左检测到围栏
                if fence == 5:
                    self.controller.move_cmd(-400, -400)
                    time.sleep(0.4)
                # 前右检测到围栏
                if fence == 6:
                    self.controller.move_cmd(-400, -400)
                    time.sleep(0.4)
                # 后有检测到围栏
                if fence == 7:
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.4)
                # 后左检测到围栏
                if fence == 8:
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.4)
                # 前方或后方有台上敌人
                if fence == 9:
                    self.controller.move_cmd(500, -500)
                    time.sleep(0.3)
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.4)
                # 左侧或右侧有台上敌人
                if fence == 10:
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.4)
                # 前方、左侧和右侧检测到围栏
                if fence == 11:
                    self.controller.move_cmd(-400, -300)
                    time.sleep(0.5)
                    self.controller.move_cmd(-400, 400)
                    time.sleep(0.3)
                # 前右后检测到围栏
                if fence == 12:
                    self.controller.move_cmd(300, 600)
                    time.sleep(0.4)
                # 前左后检测到围栏
                if fence == 13:
                    self.controller.move_cmd(600, 300)
                    time.sleep(0.4)
                # 右左后检测到围栏
                if fence == 14:
                    self.controller.move_cmd(-400, 400)
                    time.sleep(0.2)
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.3)
                # 前右检测到擂台
                if fence == 15:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(360, -400)
                            time.sleep(0.002)
                #  前左检测到擂台
                if fence == 16:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(-400, 400)
                            time.sleep(0.002)
                # 在台下，后方和右侧对擂台其他传感器没检测到
                if fence == 17:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(400, -500)
                            time.sleep(0.002)
                # 在台下，后方和左侧对擂台其他传感器没检测到
                if fence == 18:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[1]
                        ad4 = self.controller.adc_data[4]
                        ad6 = self.controller.adc_data[6]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(400, 400)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(-420, 350)
                            time.sleep(0.002)
            if stage == 1:
                self.na = 0
                self.nb = 0
                edge = self.edge_detect()
                if edge == 0:
                    enemy = self.enemy_detect()
                    # 无敌人
                    if enemy == 0:
                        self.controller.move_cmd(350, 350)
                        time.sleep(0.01)
                    # 前有qizi
                    if enemy == 1:
                        self.controller.move_cmd(700, 700)
                        time.sleep(0.02)
                    # 右侧有敌人
                    if enemy == 2:
                        self.controller.move_cmd(-400, -400)
                        time.sleep(0.1)
                        self.controller.move_cmd(400, -400)
                        time.sleep(0.5)
                    # 后方有敌人
                    if enemy == 3:
                        self.controller.move_cmd(-400, 400)
                        time.sleep(1.0)
                    # 左侧有敌人
                    if enemy == 4:
                        self.controller.move_cmd(-400, -400)
                        time.sleep(0.2)
                        self.controller.move_cmd(-400, 400)
                        time.sleep(0.5)
                    if enemy == 5:
                        self.controller.move_cmd(-400, -400)
                        time.sleep(0.2)
                        self.controller.move_cmd(-400, 400)
                        time.sleep(0.5)
                        self.controller.move_cmd(400, 400)
                        time.sleep(0.4)
                    # 前方检测到箱子
                    if enemy == 11:
                        self.controller.move_cmd(800, 800)
                        time.sleep(0.02)
                # 左前检测到边缘
                if edge == 1:
                    self.controller.move_cmd(-400, -400)
                    time.sleep(0.4)
                    self.controller.move_cmd(400, -400)
                    time.sleep(0.5)
                # 右前检测到边缘
                if edge == 2:
                    self.controller.move_cmd(-400, -400)
                    time.sleep(0.4)
                    self.controller.move_cmd(-400, 400)
                    time.sleep(0.3)
                # 右后检测到边缘
                if edge == 3:
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.5)
                    self.controller.move_cmd(400, -400)
                    time.sleep(0.5)
                # 左后检测到边缘
                if edge == 4:
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.5)
                    self.controller.move_cmd(-400, 400)
                    time.sleep(0.5)
                # 前方两个检测到边缘
                if edge == 5:
                    self.controller.move_cmd(-500, -500)
                    time.sleep(0.7)
                    self.controller.move_cmd(500, -500)
                    time.sleep(0.3)
                # 后方两个检测到边缘
                if edge == 6:
                    self.controller.move_cmd(500, 500)
                    time.sleep(0.5)
                # 左侧两个检测到边缘
                if edge == 7:
                    self.controller.move_cmd(500, -400)
                    time.sleep(0.5)
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.3)
                # 右侧两个检测到边缘
                if edge == 8:
                    self.controller.move_cmd(-400, 500)
                    time.sleep(0.5)
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.3)
                # 搁浅前在底下
                if edge == 9:
                    self.nd += 1
                    if self.nd > 20:
                        self.nd = 0
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.controller.move_cmd(-500, -500)
                        time.sleep(0.2)
                        self.go_up_ahead_platform()
                        self.controller.move_cmd(-500, -500)
                        time.sleep(0.8)
                        self.default_platform()
                        self.controller.move_cmd(-500, -500)
                        time.sleep(0.5)
                        self.controller.move_cmd(500, -500)
                        time.sleep(0.3)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.02)
                if edge == 10:
                    self.ne += 1
                    if self.ne > 20:
                        self.ne = 0
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.controller.move_cmd(500, 500)
                        time.sleep(0.2)
                        self.go_up_ahead_platform()
                        self.controller.move_cmd(500, 500)
                        time.sleep(0.8)
                        self.default_platform()
                        self.controller.move_cmd(500, 500)
                        time.sleep(0.4)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.02)
                if edge == 102:
                    self.controller.move_cmd(500, 500)
                    time.sleep(0.01)
            # 搁浅左侧在擂台右侧在地面
            if stage == 3:
                self.na += 1
                if self.na == 350:
                    self.controller.move_cmd(-500, 500)
                    self.controller.up.CDS_SetAngle(5, 1000, self.servo_speed)
                    self.controller.up.CDS_SetAngle(7, 24, self.servo_speed)
                    time.sleep(0.8)
                    self.default_platform()
                    time.sleep(0.6)
                    self.na = 0
                else:
                    time.sleep(0.001)
            # 搁浅右侧在擂台左侧在地面
            if stage == 4:
                self.na += 1
                if self.na == 350:
                    self.controller.move_cmd(500, -500)
                    self.controller.up.CDS_SetAngle(6, 24, self.servo_speed)
                    self.controller.up.CDS_SetAngle(8, 1000, self.servo_speed)
                    time.sleep(0.8)
                    self.default_platform()
                    time.sleep(0.6)
                    self.na = 0
                else:
                    time.sleep(0.001)
    
    def mortor_test(self):
        self.controller.move_cmd(400, -400)
        time.sleep(0.7)
        self.controller.move_cmd(0, 0)

    def stop(self):
        self.controller.move_cmd(0, 0)


if __name__ == '__main__':
    match_demo = MatchDemo()
    # match_demo.stop()
    match_demo.start_match()