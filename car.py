#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController

class CAR:

    def __init__(self):
        self.up=uptech.UpTech()
        self.up.ADC_IO_Open()
        self.up.LCD_Open(2)    
        self.up.ADC_Led_SetColor(0,0x07E0)          #led绿色
        self.up.ADC_Led_SetColor(1,0x07E0)
        self.up.LCD_PutString(10, 0, 'uptech_car')
        self.up.LCD_Refresh()                       #刷新屏幕
        self.up_controller=UpController()
        servo_ids = [1,2,3,4]
        self.up_controller.set_cds_mode(servo_ids,1)#电机模式
  
    def start(self):
        while True:
            if  self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==1:      #前进
                self.up.ADC_Led_SetColor(0,0x0000)
                self.up.ADC_Led_SetColor(1,0x0000)
                self.up_controller.move_cmd(500,500)
                time.sleep(0.2)
            elif self.up_controller.io_data[1]==0:                    #左转
                self.up.ADC_Led_SetColor(0,0xF800)
                self.up.ADC_Led_SetColor(1,0X0000)
                self.up_controller.move_cmd(-500,-500)
                time.sleep(1)
                self.up_controller.move_cmd(-500,500)
                time.sleep(1)
            else:                                 #右转
                self.up.ADC_Led_SetColor(0,0x0000)
                self.up.ADC_Led_SetColor(1,0XF800)
                self.up_controller.move_cmd(-500,-500)
                time.sleep(1)
                self.up_controller.move_cmd(500,-500)
                time.sleep(1)
        
if __name__ == '__main__':
    car = CAR()
    car.start()

   
       
        
        
    
            

    





