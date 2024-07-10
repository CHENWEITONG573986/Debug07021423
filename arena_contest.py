import cv2
import apriltag
import sys
import numpy as np
from up_controller import UpController
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

class ArenaContest:
    def __init__(self):
        self.target_id = 0
        self.detect_flag = False
        self.up_flag = False
        self.tag_one_flag = False
        self.tag_two_flag = True
        self.stop_count = 0
        self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        BaseManager.register('UpController', UpController)
        manager = BaseManager()
        manager.start()
        self.up = manager.UpController()
        controller_up = Process(name="controller_up", target=self.controller_init)
        controller_up.start()
        self.apriltag_width = 0
        

    def controller_init(self):
        print("process start")
        self.up.lcd_display("ArenaContest")
        self.up.set_chassis_mode(2)
        motor_ids = [1,2]
        servo_ids = [5,6,7,8]
        self.up.set_cds_mode(motor_ids, 1)
        self.up.set_cds_mode(servo_ids, 0)
        self.up.open_edge_detect()
        
        #self.up.go_up_platform()
        
    
    def update_frame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tags = self.at_detector.detect(gray)
        for tag in tags:
            cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
            cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
            cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
            cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
            self.apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2 + tag.corners[0][0] + self.apriltag_width
        #apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2
        
        if len(tags) > 0 and self.detect_flag is not True:
            target_x = self.apriltag_width / len(tags)
            self.apriltag_width = 0
            print(target_x)
            self.stop_count += 1
            if self.stop_count == 3:
                self.up.set_controller_cmd(6)
                self.stop_count = 0
            if target_x < 280:
                # print("move_left")
                self.up.set_controller_cmd(4)
            elif target_x > 300:
                # print("move_right")
                self.up.set_controller_cmd(5)
            else:
                self.up.set_controller_cmd(6)
                self.detect_flag = True
                self.apriltag_width = 0

        elif self.detect_flag and self.up_flag is not True:
            print("move_up")
            self.up.set_controller_cmd(1)
            self.up_flag = True
        elif self.up_flag is not True:
            self.up.set_controller_cmd(4)

        


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    ac = ArenaContest()
    while True:
        ret, frame = cap.read()
        ac.update_frame(frame)
        cv2.imshow("img", frame)
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

