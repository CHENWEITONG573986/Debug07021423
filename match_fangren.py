import threading
from typing import Tuple
from up_controller import UpController
import time
import cv2
import apriltag
import sys
import numpy as np


class MatchFangren:
    def __init__(self):
        self.version = "v1.0"
        self.controller = UpController()
        self.controller.lcd_display("MatchFangren")
        servo_ids = [3, 4, 5, 6, 7, 8, 11, 12]
        self.controller.set_cds_mode(servo_ids, 0)
        self.k = 0
        self.r = 0
        self.m = 0
        self.nh = 0
        self.nq = 0
        self.apriltag_state = 0
    
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
            # frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tags = self.at_detector.detect(gray)
            self.tag_id = -1
            self.tag_len = len(tags)
            for tag in tags:
                self.tag_id = tag.tag_id
                cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
                cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
                cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
                cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
                self.apriltag_width = 0
                if tag.tag_id == 0:
                    self.apriltag_state = 1
                    self.apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2 + tag.corners[0][0] + self.apriltag_width
                    target_x = self.apriltag_width / self.tag_len
                    self.apriltag_width = 0
                    print(target_x)
                    if target_x < 280:
                        self.controller.move_cmd(-230, 230)
                    elif target_x > 330:
                        self.controller.move_cmd(230, -230)
                    else:
                        self.controller.move_cmd(270, 270)
                        time.sleep(3)
                        self.controller.move_cmd(0, 0)
                        self.attack_tag()
                        self.apriltag_state = 0
            cv2.imshow("img", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    # 默认动作
    def default_action(self):
        self.controller.up.CDS_SetAngle(3, 512, 512)
        self.controller.up.CDS_SetAngle(4, 75, 512)
        self.controller.up.CDS_SetAngle(5, 307, 512)
        self.controller.up.CDS_SetAngle(6, 512, 512)
        self.controller.up.CDS_SetAngle(7, 949, 512)
        self.controller.up.CDS_SetAngle(8, 717, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)

    # 前倾倒起立动作
    def ahead_dump(self):
        self.controller.up.CDS_SetAngle(3, 512, 512)
        self.controller.up.CDS_SetAngle(4, 75, 512)
        self.controller.up.CDS_SetAngle(5, 307, 512)
        self.controller.up.CDS_SetAngle(6, 512, 512)
        self.controller.up.CDS_SetAngle(7, 949, 512)
        self.controller.up.CDS_SetAngle(8, 717, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(1.5)
        self.controller.up.CDS_SetAngle(3, 82, 812)
        self.controller.up.CDS_SetAngle(6, 942, 812)
        self.controller.up.CDS_SetAngle(11, 462, 512)
        self.controller.up.CDS_SetAngle(12, 562, 512)
        time.sleep(2)
        self.controller.up.CDS_SetAngle(4, 375, 512)
        self.controller.up.CDS_SetAngle(7, 649, 512)
        time.sleep(0.5)
        self.controller.up.CDS_SetAngle(3, 112, 812)
        self.controller.up.CDS_SetAngle(4, 512, 512)
        self.controller.up.CDS_SetAngle(5, 512, 512)
        self.controller.up.CDS_SetAngle(6, 912, 812)
        self.controller.up.CDS_SetAngle(7, 512, 512)
        self.controller.up.CDS_SetAngle(8, 512, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(2)
        self.controller.up.CDS_SetAngle(3, 262, 812)
        self.controller.up.CDS_SetAngle(6, 762, 812)
        self.controller.up.CDS_SetAngle(11, 712, 512)
        self.controller.up.CDS_SetAngle(12, 312, 512)
        time.sleep(1.5)
        self.controller.up.CDS_SetAngle(5, 312, 812)
        self.controller.up.CDS_SetAngle(8, 712, 812)
        time.sleep(0.5)
        self.controller.up.CDS_SetAngle(3, 512, 512)
        self.controller.up.CDS_SetAngle(4, 75, 512)
        self.controller.up.CDS_SetAngle(5, 307, 512)
        self.controller.up.CDS_SetAngle(6, 512, 512)
        self.controller.up.CDS_SetAngle(7, 949, 512)
        self.controller.up.CDS_SetAngle(8, 717, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        return
        self.controller.move_cmd(500, 500)
        time.sleep(0.3)
        self.controller.move_cmd(0, 0)
        time.sleep(0.01)

    # 前倾倒起立动作
    def behind_dump(self):
        self.controller.up.CDS_SetAngle(3, 512, 512)
        self.controller.up.CDS_SetAngle(4, 75, 512)
        self.controller.up.CDS_SetAngle(5, 307, 512)
        self.controller.up.CDS_SetAngle(6, 512, 512)
        self.controller.up.CDS_SetAngle(7, 949, 512)
        self.controller.up.CDS_SetAngle(8, 717, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(1.5)
        self.controller.up.CDS_SetAngle(3, 942, 812)
        self.controller.up.CDS_SetAngle(6, 82, 812)
        self.controller.up.CDS_SetAngle(11, 562, 512)
        self.controller.up.CDS_SetAngle(12, 462, 512)
        time.sleep(2)
        self.controller.up.CDS_SetAngle(4, 375, 512)
        self.controller.up.CDS_SetAngle(7, 649, 512)
        time.sleep(0.5)
        self.controller.up.CDS_SetAngle(3, 912, 812)
        self.controller.up.CDS_SetAngle(4, 512, 512)
        self.controller.up.CDS_SetAngle(5, 512, 512)
        self.controller.up.CDS_SetAngle(6, 112, 812)
        self.controller.up.CDS_SetAngle(7, 512, 512)
        self.controller.up.CDS_SetAngle(8, 512, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(2)
        self.controller.up.CDS_SetAngle(3, 762, 812)
        self.controller.up.CDS_SetAngle(6, 262, 812)
        self.controller.up.CDS_SetAngle(11, 362, 512)
        self.controller.up.CDS_SetAngle(12, 662, 512)
        time.sleep(1.5)
        self.controller.up.CDS_SetAngle(5, 312, 812)
        self.controller.up.CDS_SetAngle(8, 712, 812)
        time.sleep(0.5)
        self.controller.up.CDS_SetAngle(3, 512, 512)
        self.controller.up.CDS_SetAngle(4, 75, 512)
        self.controller.up.CDS_SetAngle(5, 307, 512)
        self.controller.up.CDS_SetAngle(6, 512, 512)
        self.controller.up.CDS_SetAngle(7, 949, 512)
        self.controller.up.CDS_SetAngle(8, 717, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        self.controller.move_cmd(-500, -500)
        time.sleep(0.3)
        self.controller.move_cmd(0, 0)
        time.sleep(0.01)

    def attack_a(self):
        self.controller.up.CDS_SetAngle(3, 312, 512)
        self.controller.up.CDS_SetAngle(4, 812, 512)
        self.controller.up.CDS_SetAngle(5, 412, 512)
        self.controller.up.CDS_SetAngle(6, 812, 512)
        self.controller.up.CDS_SetAngle(7, 212, 512)
        self.controller.up.CDS_SetAngle(8, 612, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(2)
        self.controller.up.CDS_SetAngle(3, 152, 512)
        self.controller.up.CDS_SetAngle(4, 712, 512)
        self.controller.up.CDS_SetAngle(5, 312, 512)
        self.controller.up.CDS_SetAngle(6, 862, 512)
        self.controller.up.CDS_SetAngle(7, 312, 512)
        self.controller.up.CDS_SetAngle(8, 712, 512)
        self.controller.up.CDS_SetAngle(11, 522, 512)
        self.controller.up.CDS_SetAngle(12, 502, 512)
        time.sleep(1)
        self.controller.move_cmd(300, 300)
        time.sleep(1)
        self.controller.move_cmd(0, 0)

    def attack_tag(self):
        # self.controller.up.CDS_SetAngle(3, 356, 512)
        # self.controller.up.CDS_SetAngle(4, 512, 1000)
        # self.controller.up.CDS_SetAngle(5, 512, 1000)
        self.controller.up.CDS_SetAngle(6, 700, 512)
        self.controller.up.CDS_SetAngle(7, 300, 1000)
        self.controller.up.CDS_SetAngle(8, 400, 1000)
        time.sleep(1)
        # self.controller.up.CDS_SetAngle(6, 700, 512)
        self.controller.up.CDS_SetAngle(7, 512, 1000)
        self.controller.up.CDS_SetAngle(8, 521, 1000)
        # self.controller.up.CDS_SetAngle(11, 522, 512)
        # self.controller.up.CDS_SetAngle(12, 502, 512)
        time.sleep(2)

    def attack_b(self):
        self.controller.up.CDS_SetAngle(3, 122, 512)
        self.controller.up.CDS_SetAngle(4, 512, 1000)
        self.controller.up.CDS_SetAngle(5, 512, 1000)
        self.controller.up.CDS_SetAngle(6, 892, 512)
        self.controller.up.CDS_SetAngle(7, 512, 1000)
        self.controller.up.CDS_SetAngle(8, 512, 1000)
        self.controller.up.CDS_SetAngle(11, 522, 512)
        self.controller.up.CDS_SetAngle(12, 502, 512)
        time.sleep(2)

    def attack_c(self):
        self.controller.up.CDS_SetAngle(3, 132, 512)
        self.controller.up.CDS_SetAngle(4, 712, 512)
        self.controller.up.CDS_SetAngle(5, 312, 512)
        self.controller.up.CDS_SetAngle(6, 852, 512)
        self.controller.up.CDS_SetAngle(7, 312, 512)
        self.controller.up.CDS_SetAngle(8, 712, 512)
        self.controller.up.CDS_SetAngle(11, 522, 512)
        self.controller.up.CDS_SetAngle(12, 502, 512)
        time.sleep(2)

    def attack_d(self):
        self.controller.up.CDS_SetAngle(3, 112, 512)
        self.controller.up.CDS_SetAngle(4, 362, 512)
        self.controller.up.CDS_SetAngle(5, 512, 512)
        self.controller.up.CDS_SetAngle(6, 932, 512)
        self.controller.up.CDS_SetAngle(7, 462, 512)
        self.controller.up.CDS_SetAngle(8, 512, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(2)
        self.controller.move_cmd(0, 0)

    def attack_e(self):
        self.controller.up.CDS_SetAngle(3, 92, 512)
        self.controller.up.CDS_SetAngle(4, 562, 512)
        self.controller.up.CDS_SetAngle(5, 512, 512)
        self.controller.up.CDS_SetAngle(6, 942, 512)
        self.controller.up.CDS_SetAngle(7, 662, 512)
        self.controller.up.CDS_SetAngle(8, 512, 512)
        self.controller.up.CDS_SetAngle(11, 512, 512)
        self.controller.up.CDS_SetAngle(12, 512, 512)
        time.sleep(2)
        self.controller.move_cmd(0, 0)

    def attack_f(self):
        self.controller.up.CDS_SetAngle(3, 152, 512)
        self.controller.up.CDS_SetAngle(4, 312, 512)
        self.controller.up.CDS_SetAngle(5, 312, 512)
        self.controller.up.CDS_SetAngle(6, 862, 512)
        self.controller.up.CDS_SetAngle(7, 712, 512)
        self.controller.up.CDS_SetAngle(8, 512, 512)
        self.controller.up.CDS_SetAngle(11, 522, 512)
        self.controller.up.CDS_SetAngle(12, 502, 512)
        time.sleep(2)
        self.controller.move_cmd(0, 0)

    # 机器倾斜检测
    def angle_detect(self):
        ad2 = self.controller.adc_data[2]
        # print("ad3 = {},ad6 = {},ad7 = {}".format(self.controller.adc_data[3],self.controller.adc_data[6],self.controller.adc_data[7]))
        # 没有倒
        if 1428 < ad2 < 2628:
            return 1
        # 前倾
        elif ad2 < 1200:
            return 2
        # 后倾
        elif 1800 < ad2 < 2600:
            return 3
        # 边缘状态
        else:
            return 0

    # 敌人检测
    def enemy_detect(self):
        # 头部红外测距传感器
        ad0 = self.controller.adc_data[0]
        # 倾角传感器
        ad2 = self.controller.adc_data[2]
        # 左侧红外测距传感器
        ad3 = self.controller.adc_data[3]
        # 前边沿红外测距传感器
        ad4 = self.controller.adc_data[4]
        # 灰度传感器
        ad5 = self.controller.adc_data[5]
        # 左红外测距传感器
        ad6 = self.controller.adc_data[6]
        # 右红外测距传感器
        ad7 = self.controller.adc_data[7]
        if self.apriltag_state == 1:
            return 11
        else:
            if ad5 > 2450:
                # 左有敌人
                if ad6 < 350 and ad3 > 700 and ad7 < 310:
                    return 4
                # 无敌人，无边缘
                elif ad6 < 350 and ad3 < 700 and ad7 < 310:
                    if self.tag_id == 1:
                        return 11
                    else:
                        return 1
                # 前右有敌人
                elif ad6 < 350 and ad3 < 700 and ad7 > 310:
                    return 5
                elif ad6 < 350 and ad3 > 700 and ad7 > 310:
                    return 0
                # # 前敌人
                elif ad6 > 350 and ad3 < 700 and ad7 < 310:
                    return 7
                # 前敌人
                # elif ad6 > 350 and ad3 > 700 and ad7 < 310:
                #     return 7
                # # 前敌人
                # elif ad6 > 350 and ad3 < 700 and ad7 > 310:
                #     return 7
                # elif self.tag_id == 0:
                #     return 0

                # elif ad6 > 350 and ad3 > 700 and ad7 > 310:
                #     return 7
                else:
                    return 0
            # 无敌人前方到边缘
            elif ad5 <= 2450 and self.tag_id != 0:
                return 2
            else:
                return 0


    def test_servo(self):
        self.controller.move_cmd(400, 500)

    # 开始比赛
    def start_match(self):
    
        self.default_action()
        time.sleep(0.8)
        self.controller.up.CDS_SetAngle(3, 102, 512)
        self.controller.up.CDS_SetAngle(6, 922, 512)
        self.controller.up.CDS_SetAngle(11, 922, 512)
        self.controller.up.CDS_SetAngle(12, 102, 512)
        while True:
            ad3 = self.controller.adc_data[3]
            if ad3 > 1000:
                break
            time.sleep(0.01)

        self.controller.move_cmd(300, 400)
        time.sleep(3)
        self.default_action()
        self.controller.move_cmd(0, 0)
        time.sleep(2)

        while True:
            angle_state = self.angle_detect()
            # print("angle_state = {}".format(angle_state))
            # 没倾倒
            if angle_state == 1:
                edge = self.enemy_detect()
                # print(edge)
                # 无敌人无边缘
                if edge == 1:
                    self.k += 1
                    if self.k > 350:
                        self.controller.move_cmd(300, -300)
                        time.sleep(0.01)
                        self.k = 0
                    else:
                        self.controller.move_cmd(300, 300)
                        time.sleep(0.01)
                    self.default_action()
                if edge == 2:
                    self.r += 1
                    if self.r < 4:
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.5)
                        self.controller.move_cmd(-350, -350)
                        time.sleep(0.5)
                        self.controller.move_cmd(300, -300)
                        time.sleep(1.3)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.default_action()
                    elif 3 < self.r < 9:
                        self.controller.move_cmd(-350, -350)
                        time.sleep(0.5)
                        self.controller.move_cmd(300, -300)
                        time.sleep(1.3)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.default_action()
                    elif self.r > 12:
                        self.r = 0
                    else:
                        self.controller.move_cmd(-350, -350)
                        time.sleep(0.5)
                        self.controller.move_cmd(-300, 300)
                        time.sleep(0.5)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.default_action()
                # 左侧有低人
                if edge == 4:
                    self.controller.move_cmd(-300, -300)
                    time.sleep(0.45)
                    self.controller.move_cmd(-300, 300)
                    time.sleep(0.35)
                    self.controller.move_cmd(300, 300)
                    time.sleep(0.35)
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.01)
                    ad6 = self.controller.adc_data[6]
                    if ad6 > 2000:
                        self.controller.move_cmd(300, 300)
                        self.attack_b()
                        time.sleep(1.4)
                        self.controller.move_cmd(0, 0)
                    # else:
                    #     self.controller.move_cmd(-300, -300)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(400, -400)
                    #     time.sleep(0.2)
                # 前右敌人
                if edge == 5:
                    self.controller.move_cmd(300, -300)
                    time.sleep(0.1)
                    self.controller.move_cmd(400, 400)
                    time.sleep(0.35)
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.01)
                    ad6 = self.controller.adc_data[6]
                    if ad6 > 2000:
                        self.controller.move_cmd(300, 300)
                        self.attack_b()
                        time.sleep(1.4)
                        self.controller.move_cmd(0, 0)
                    # else:
                    #     self.controller.move_cmd(-300, -300)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(400, -400)
                    #     time.sleep(0.2)
                #  正前方有敌人
                if edge == 7:
                    self.attack_a()
                    self.controller.move_cmd(300, 300)
                    time.sleep(1.4)
                    self.controller.move_cmd(0, 0)
                    # print("ssss")
                    # self.m += 1
                    # self.controller.move_cmd(-500, -400)
                    # time.sleep(0.9)
                    # self.attack_c()
                    # self.controller.move_cmd(0, 0)
                    # time.sleep(0.6)
                    # self.controller.move_cmd(500, 500)
                    # time.sleep(0.3)
                    # self.controller.move_cmd(300, 300)
                    # time.sleep(0.5)
                    # ad0 = self.controller.adc_data[0]
                    # ad1 = self.controller.adc_data[1]
                    # ad6 = self.controller.adc_data[6]
                    # if (ad1 < 300 or ad0 > 80 or ad6 > 120) and self.m == 1:
                    #     self.controller.move_cmd(300, 300)
                    #     time.sleep(0.1)
                    #     self.attack_b()
                    #     time.sleep(0.4)
                    #     self.attack_c()
                    #     time.sleep(0.4)
                    #     self.controller.move_cmd(400, 400)
                    #     time.sleep(0.01)
                    #     self.attack_b()
                    #     time.sleep(0.4)
                    #     self.controller.move_cmd(600, 600)
                    #     time.sleep(1)
                    #     self.controller.move_cmd(400, 400)
                    #     time.sleep(1)
                    #     self.controller.move_cmd(300, 300)
                    #     time.sleep(0.5)
                    #     self.controller.move_cmd(200, 200)
                    #     time.sleep(0.3)
                    #     self.controller.move_cmd(-500, -400)
                    #     time.sleep(0.8)
                    #     self.controller.move_cmd(0, 0)
                    #     time.sleep(0.01)
                    #     self.m = 0
                    # else:
                    #     self.controller.move_cmd(100, 100)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(0, 0)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(-300, -300)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(400, -400)
                    #     time.sleep(0.2)
                    #     self.m = 0
                # if edge == 11:
                    
            # 前倾
            if angle_state == 2:
                self.nq += 1
                if self.nq == 6:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.1)
                    self.default_action()
                    time.sleep(0.8)
                    self.ahead_dump()
                    time.sleep(0.5)
                    self.nq = 0
                else:
                    time.sleep(0.04)
            # 后倾
            if angle_state == 3:
                self.nh += 1
                if self.nh == 6:
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.1)
                    self.default_action()
                    time.sleep(0.8)
                    self.behind_dump()
                    time.sleep(0.5)
                    self.nh = 0
                else:
                    time.sleep(0.05)

            if angle_state == 0:
                self.controller.move_cmd(200, 200)
                time.sleep(0.01)

if __name__ == '__main__':
    match = MatchFangren()
    
    # while True:
    #     match.angle_detect()
    match.start_match()