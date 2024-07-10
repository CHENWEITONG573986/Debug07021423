#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
import threading

class Controller:

    # cmd
    NO_CONTROLLER = 0
    MOVE_UP = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    MOVE_FORWARD= 4
    MOVE_BACKWARD = 5
    MOVE_STOP = 6
    PICK_UP_YELLOW = 7
    PICK_UP_GREEN = 8
    SPEED_UP = 9
    SPEED_DOWN = 10
    SPEED = 200

    # chassis_mode 1 for servo ,2 for controller
    CHASSIS_MODE_SERVO = 1
    CHASSIS_MODE_CONTROLLER = 2


    def __init__(self):
        self.up=uptech.UpTech()
        self.up.LCD_Open(2)
        self.up.ADC_IO_Open()
        self.up.CDS_Open()

        self.cmd = 0
        self.adc_data = []
        self.io_data = []
        controller_thread = threading.Thread(name = "up_controller_thread",target=self.send_cmd)
        controller_thread.setDaemon(True)
        controller_thread.start()
        self.pick_flag = False

    def set_chassis_mode(self,mode):
        self.chassis_mode = mode

    def send_cmd(self):
        """控制舵机运动
        通过不同的命令控制机器人的不同状态
        """        
        while True:
            if self.cmd == self.MOVE_UP:
                self.move_up()
            if self.cmd == self.MOVE_LEFT:
                self.move_left()
            if self.cmd == self.MOVE_RIGHT:
                self.move_right()
            if self.cmd == self.MOVE_FORWARD:
                self.move_forward()
            if self.cmd == self.MOVE_BACKWARD:
                self.move_backward()
            if self.cmd == self.MOVE_STOP:
                self.move_stop()
            if self.cmd == self.PICK_UP_YELLOW:
                self.pick_up_yellow()   
            if self.cmd == self.PICK_UP_GREEN:
                self.pick_up_green()   
            if self.cmd == self.SPEED_UP:
                self.speed_up() 
            if self.cmd == self.SPEED_DOWN:
                self.speed_down()

    def speed_up(self):
        """机器人加速
        舵机速度调大
        :return: 无
        """
        self.SPEED = 250
        self.cmd = self.NO_CONTROLLER    

    def speed_down(self):
        """机器人减速
        舵机速度调小
        :return: 无
        """
        self.SPEED = 160
        self.cmd = self.NO_CONTROLLER                      
    def get_ad_data(self):
        return self.adc_data

    def move_left(self):
        """机器人向左移动
        1,2号舵机速度调为负值, 3,4号舵机速度为正值
        :return: 无
        """
        self.up.CDS_SetSpeed(1, -self.SPEED)
        self.up.CDS_SetSpeed(2, -self.SPEED)
        self.up.CDS_SetSpeed(3, self.SPEED)
        self.up.CDS_SetSpeed(4, self.SPEED) 
        self.cmd = self.NO_CONTROLLER

    def move_right(self):
        """机器人向右移动
        1,2号舵机速度为正值, 3,4号舵机速度调为负值
        :return: 无
        """
        self.up.CDS_SetSpeed(1, self.SPEED)
        self.up.CDS_SetSpeed(2, self.SPEED)
        self.up.CDS_SetSpeed(3, -self.SPEED)
        self.up.CDS_SetSpeed(4, -self.SPEED) 
        self.cmd = self.NO_CONTROLLER

    def move_forward(self):
        """机器人向前移动
        1,3号舵机速度为正值, 2,4号舵机速度调为负值
        :return: 无
        """
        self.up.CDS_SetSpeed(1, self.SPEED)
        self.up.CDS_SetSpeed(2, -self.SPEED)
        self.up.CDS_SetSpeed(3, self.SPEED)
        self.up.CDS_SetSpeed(4, -self.SPEED) 
        self.cmd = self.NO_CONTROLLER

    def move_backward(self):
        """机器人向后移动
        1,3号舵机速度调为负值, 2,4号舵机速度为正值
        :return: 无
        """
        self.up.CDS_SetSpeed(1, -self.SPEED)
        self.up.CDS_SetSpeed(2, self.SPEED)
        self.up.CDS_SetSpeed(3, -self.SPEED)
        self.up.CDS_SetSpeed(4, self.SPEED) 
        self.cmd = self.NO_CONTROLLER

    def move_stop(self):
        """机器人停止移动
        1,2,3,4号舵机速度调整为0
        :return: 无
        """
        self.up.CDS_SetSpeed(1, 0)
        self.up.CDS_SetSpeed(2, 0)
        self.up.CDS_SetSpeed(3, 0)
        self.up.CDS_SetSpeed(4, 0) 
        self.cmd = self.NO_CONTROLLER

    def pick_up_yellow(self):
        """捡黄球
        按照既定流程进行捡球
        :return: 无
        """
        print("**********开始捡黄球**********")
        self.move_stop()
        self.up.CDS_SetAngle(9,400,250)  # 张爪
        print("张爪")
        time.sleep(1)
        self.up.CDS_SetAngle(8,650,250)  # 爪子前移
        print("爪子前移")
        time.sleep(1)        
        self.up.CDS_SetAngle(6,650,250)  # 低头靠近物料
        print("低头靠近物料")
        time.sleep(1)
        self.up.CDS_SetAngle(9,550,250)  # 收爪
        print("收爪")
        time.sleep(1)
        self.up.CDS_SetAngle(6,400,250)  # 抬头
        print("抬头")
        time.sleep(1)
        self.up.CDS_SetAngle(5,750,250)  # 向左转体
        print("向左转体")
        time.sleep(1)
        self.up.CDS_SetAngle(8,460,250)  # 爪子后移
        print("爪子后移")
        time.sleep(1)          
        self.up.CDS_SetAngle(9,400,250)  # 张爪
        print("张爪")
        time.sleep(1)
        self.cmd = self.NO_CONTROLLER
        self.servo_reset()
        print("**********结束捡黄球**********")


    def pick_up_green(self):
        """捡绿球
        按照既定流程捡绿球
        :return: 无
        """
        print("**********开始捡绿球**********")
        self.move_stop()
        self.up.CDS_SetAngle(9,400,250)  # 张爪
        print("张爪")
        time.sleep(1)
        self.up.CDS_SetAngle(8,650,250)  # 爪子前移
        print("爪子前移")
        time.sleep(1)        
        self.up.CDS_SetAngle(6,650,250)  # 低头靠近物料
        print("低头靠近物料")
        time.sleep(1)
        self.up.CDS_SetAngle(9,550,250)  # 收爪
        print("收爪")
        time.sleep(1)
        self.up.CDS_SetAngle(6,400,250)  # 抬头
        print("抬头")
        time.sleep(1)
        self.up.CDS_SetAngle(5,200,250)  # 向右转体
        print("向右转体")
        time.sleep(1)
        self.up.CDS_SetAngle(8,460,250)  # 爪子后移
        print("爪子后移")
        time.sleep(1)          
        self.up.CDS_SetAngle(9,400,250)  # 张爪
        print("张爪")
        time.sleep(1)
        self.cmd = self.NO_CONTROLLER
        self.servo_reset()
        print("**********结束捡绿球**********")

    def servo_reset(self):
        """机器人复位
        将所有舵机的值设置为初始状态值(可自行指定)
        """
        self.up.CDS_SetAngle(5,480,self.SPEED)
        time.sleep(1)
        self.up.CDS_SetAngle(6,520,self.SPEED)
        time.sleep(1)
        self.up.CDS_SetAngle(7,512,self.SPEED)
        time.sleep(1)
        self.up.CDS_SetAngle(8,512,self.SPEED)
        time.sleep(1)
        self.up.CDS_SetAngle(9,400,self.SPEED)
        time.sleep(1)

    def set_cds_mode(self,ids,mode):
        for id in ids:
            self.up.CDS_SetMode(id,mode)

    def set_controller_cmd(self,cmd):
        self.cmd = cmd

    def get_controller_cmd(self):
        return self.cmd

    def lcd_display(self,content):
        self.up.LCD_PutString(30, 0, content)
        self.up.LCD_Refresh()
        self.up.LCD_SetFont(self.up.FONT_8X14)


if __name__ == '__main__':
    ctrl = Controller()
    ctrl.servo_reset()
    ctrl.move_stop()

    



