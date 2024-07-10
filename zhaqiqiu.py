#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController

class ZHAQIQIU:

    def __init__(self):
        self.up = uptech.UpTech()
        self.up_controller = UpController()
        self.up.ADC_IO_Open()
        self.up.LCD_Open(2)
        self.up.ADC_Led_SetColor(0, 0x07E0)
        self.up.ADC_Led_SetColor(1, 0x07E0)
        self.up.LCD_PutString(10, 0, 'zhaqiqiu')
        self.up.LCD_Refresh()
        self.up.CDS_Open()
        moto_ids = [1, 2, 3, 4]
        servo_ids = [5, 6]
        self.up_controller.set_cds_mode(moto_ids, 1)  # 设置舵机为电机模式
        self.up_controller.set_cds_mode(servo_ids, 0)  # 设置舵机为舵机模式
        self.up_controller.set_chassis_mode(1)    
        self.up.CDS_SetAngle(5, 512, 512)
        self.up.CDS_SetAngle(6, 512, 512)

    def start(self):
        while True:
            if self.up_controller.io_data[0] == 1 and self.up_controller.io_data[1] == 1 and self.up_controller.io_data[2] == 1:
                self.up_controller.move_up()
                time.sleep(0.2)
            if self.up_controller.io_data[0] == 0 and self.up_controller.io_data[1] == 0 and self.up_controller.io_data[2] == 0:
                self.up_controller.move_cmd(-500,-500)
                time.sleep(0.2)
            if self.up_controller.io_data[0] == 0 and self.up_controller.io_data[1] == 1 and self.up_controller.io_data[2] == 1:
                self.up_controller.move_left()
                time.sleep(0.2)
            if self.up_controller.io_data[0] == 1 and self.up_controller.io_data[1] == 1 and self.up_controller.io_data[2] == 0:
                self.up_controller.move_right()
                time.sleep(0.2)
            if self.up_controller.io_data[0] == 1 and self.up_controller.io_data[1] == 0 and self.up_controller.io_data[2] == 1:
                self.up_controller.move_stop()
                self.up.CDS_SetAngle(5, 300, 800)
                time.sleep(0.7)
                self.up.CDS_SetAngle(5, 512, 800)
                time.sleep(0.5)


if __name__ == '__main__':
    zqq = ZHAQIQIU()
    zqq.start()

    




