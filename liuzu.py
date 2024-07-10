#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController

class LIUZU:
    forward_flag = 1
    cyc = 0
    count=0

    def __init__(self):
        self.up = uptech.UpTech()
        self.up_controller = UpController()
        self.up.ADC_IO_Open()
        self.up.CDS_Open()
        servo_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.up_controller.set_cds_mode(servo_ids, 0)  # 设置舵机为舵机模式

    def ready(self):
        self.up.CDS_SetAngle(1, 512, 512)
        self.up.CDS_SetAngle(2, 512, 512)
        self.up.CDS_SetAngle(3, 512, 512)
        self.up.CDS_SetAngle(4, 512, 512)
        self.up.CDS_SetAngle(5, 512, 512)
        self.up.CDS_SetAngle(6, 512, 512)
        self.up.CDS_SetAngle(7, 512, 512)
        self.up.CDS_SetAngle(8, 512, 512)
        self.up.CDS_SetAngle(9, 512, 512)
        self.up.CDS_SetAngle(10, 512, 512)
        self.up.CDS_SetAngle(11, 512, 512)
        self.up.CDS_SetAngle(12, 512, 512)
        self.up.CDS_SetAngle(13, 512, 512)
        self.up.CDS_SetAngle(14, 512, 512)
        self.up.CDS_SetAngle(15, 512, 512)
        self.up.CDS_SetAngle(16, 512, 512)
        self.up.CDS_SetAngle(17, 512, 512)
        self.up.CDS_SetAngle(18, 512, 512)
        self.up.CDS_SetAngle(19, 512, 512)
        self.up.CDS_SetAngle(20, 512, 512)
        time.sleep(1)

    def GetState(self):
        
        global robot_state
        if self.up_controller.adc_data[1] < 180:				 				#ad没有检测到障碍————静止
            if self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==1:				#无障碍
                robot_state = 1
            elif self.up_controller.io_data[0]==0 and self.up_controller.io_data[1]==1:	      	#左侧障碍
                robot_state = 2
            elif self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==0:			#右侧障碍
                robot_state = 3
            else :  			    			 	        #后退
                robot_state = 4
        elif self.up_controller.adc_data[1] < 500:							#ad检测到障碍————幅度较大的动作
            if self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==1:				#无障碍
                robot_state = 5
            elif self.up_controller.io_data[0]==0 and self.up_controller.io_data[1]==1:	      	#左侧障碍
                robot_state = 2
            elif self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==0:			#右侧障碍
                robot_state = 3
            else :			       		 	        #后退
                robot_state = 4
        else :                  				        	#io检测到障碍————幅度较小的动作
            if self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==1:				#无障碍
                robot_state = 6
            elif self.up_controller.io_data[0]==0 and self.up_controller.io_data[1]==1:	        #左侧障碍
                robot_state = 2
            elif self.up_controller.io_data[0]==1 and self.up_controller.io_data[1]==0:			#右侧障碍
                robot_state = 3
            else :               				 	        #后退
                robot_state = 4
        if robot_state !=1 :
            self.cyc +=  1
        if self.cyc > 20:
            self.cyc = 0
            self.forward_flag = 1
        return robot_state


    def IsStateChanged(self):
        robot_state_ISC = self.GetState()
        robot_old_state = robot_state_ISC
        time.sleep(0.1)

        robot_state_ISC = self.GetState()
        if robot_old_state == robot_state_ISC:
            return 0
        else:
            robot_old_state = robot_state_ISC
            return 1


    def GoForward(self):
        
        self.count += 1

        if self.count > 5:
            self.up.CDS_SetAngle(19,512,512)
            self.up.CDS_SetAngle(20,562,512)
            time.sleep(0.5)
            self.BackSquat()
            self.ShakeHead()
            self.count = 0
            self.forward_flag = 0
            self.Standup()

        self.up.CDS_SetAngle(1,435,300)
        self.up.CDS_SetAngle(2,619,300)
        self.up.CDS_SetAngle(3,324,300)
        self.up.CDS_SetAngle(4,475,300)
        self.up.CDS_SetAngle(5,517,300)
        self.up.CDS_SetAngle(6,222,300)
        self.up.CDS_SetAngle(7,695,300)
        self.up.CDS_SetAngle(8,612,300)
        self.up.CDS_SetAngle(9,358,300)
        self.up.CDS_SetAngle(10,780,300)
        self.up.CDS_SetAngle(11,520,300)
        self.up.CDS_SetAngle(12,230,300)
        self.up.CDS_SetAngle(13,420,300)
        self.up.CDS_SetAngle(14,657,300)
        self.up.CDS_SetAngle(15,303,300)
        self.up.CDS_SetAngle(16,430,300)
        self.up.CDS_SetAngle(17,532,300)
        self.up.CDS_SetAngle(18,241,300)
        time.sleep(0.4)

        self.up.CDS_SetAngle(5,657,512)
        self.up.CDS_SetAngle(6,312,512)

        self.up.CDS_SetAngle(11,640,512)
        self.up.CDS_SetAngle(12,320,512)

        self.up.CDS_SetAngle(17,627,512)
        self.up.CDS_SetAngle(18,341,512)
        time.sleep(0.4)

        self.up.CDS_SetAngle(1,315,300)
        self.up.CDS_SetAngle(2,499,300)
        self.up.CDS_SetAngle(3,234,300)
        self.up.CDS_SetAngle(4,615,300)
        self.up.CDS_SetAngle(7,575,300)
        self.up.CDS_SetAngle(8,517,300)
        self.up.CDS_SetAngle(9,220,300)
        self.up.CDS_SetAngle(10,660,300)
        self.up.CDS_SetAngle(13,560,300)
        self.up.CDS_SetAngle(14,547,300)
        self.up.CDS_SetAngle(15,213,300)
        self.up.CDS_SetAngle(16,310,300)
        time.sleep(0.4)

        self.up.CDS_SetAngle(2,619,512)
        self.up.CDS_SetAngle(3,324,512)
        self.up.CDS_SetAngle(8,612,512)
        self.up.CDS_SetAngle(9,358,512)
        self.up.CDS_SetAngle(14,657,512)
        self.up.CDS_SetAngle(15,303,512)
        time.sleep(0.4)


    def TurnLeft(self):

        delay_TL = 0.25
        speed1_TL = 364
        speed2_TL = 273

        self.up.CDS_SetAngle(1,480,speed1_TL)
        self.up.CDS_SetAngle(2,619,100)
        self.up.CDS_SetAngle(3,334,100)
        self.up.CDS_SetAngle(4,437,speed1_TL)
        self.up.CDS_SetAngle(5,538,speed1_TL)
        self.up.CDS_SetAngle(6,365,speed2_TL)
        self.up.CDS_SetAngle(7,712,speed1_TL)
        self.up.CDS_SetAngle(8,635,100)
        self.up.CDS_SetAngle(9,330,100)
        self.up.CDS_SetAngle(10,574,speed1_TL)
        self.up.CDS_SetAngle(11,551,speed1_TL)
        self.up.CDS_SetAngle(12,395,speed2_TL)
        self.up.CDS_SetAngle(13,590,speed1_TL)
        self.up.CDS_SetAngle(14,610,100)
        self.up.CDS_SetAngle(15,278,100)
        self.up.CDS_SetAngle(16,311,speed1_TL)
        self.up.CDS_SetAngle(17,489,speed1_TL)
        self.up.CDS_SetAngle(18,392,speed2_TL)
        time.sleep(delay_TL)

        self.up.CDS_SetAngle(5,638,speed1_TL)
        self.up.CDS_SetAngle(6,290,speed2_TL)
        self.up.CDS_SetAngle(11,611,speed1_TL)
        self.up.CDS_SetAngle(12,320,speed2_TL)
        self.up.CDS_SetAngle(17,589,speed1_TL)
        self.up.CDS_SetAngle(18,317,speed2_TL)
        time.sleep(delay_TL+0.05)

        self.up.CDS_SetAngle(1,280,speed1_TL)
        self.up.CDS_SetAngle(2,519,speed1_TL)
        self.up.CDS_SetAngle(3,409,speed2_TL)
        self.up.CDS_SetAngle(4,637,speed1_TL)
        self.up.CDS_SetAngle(7,512,speed1_TL)
        self.up.CDS_SetAngle(8,535,speed1_TL)
        self.up.CDS_SetAngle(9,405,speed2_TL)
        self.up.CDS_SetAngle(10,774,speed1_TL)
        self.up.CDS_SetAngle(13,390,speed1_TL)
        self.up.CDS_SetAngle(14,510,speed1_TL)
        self.up.CDS_SetAngle(15,353,speed2_TL)
        self.up.CDS_SetAngle(16,511,speed1_TL)
        self.up.CDS_SetSpeed(2,speed1_TL)
        time.sleep(delay_TL)

        self.up.CDS_SetAngle(2,619,speed1_TL)
        self.up.CDS_SetAngle(3,334,speed2_TL)
        self.up.CDS_SetAngle(8,635,speed1_TL)
        self.up.CDS_SetAngle(9,330,speed2_TL)
        self.up.CDS_SetAngle(14,610,speed1_TL)
        self.up.CDS_SetAngle(15,278,speed2_TL)
        time.sleep(delay_TL+0.05)


    def TurnRight(self):

        delay_TR = 0.25
        speed1_TR = 364
        speed2_TR = 273


        self.up.CDS_SetAngle(1,280,speed1_TR)
        self.up.CDS_SetAngle(2,619,100)
        self.up.CDS_SetAngle(3,334,100)
        self.up.CDS_SetAngle(4,637,speed1_TR)
        self.up.CDS_SetAngle(5,538,speed1_TR)
        self.up.CDS_SetAngle(6,365,speed2_TR)
        self.up.CDS_SetAngle(7,512,speed1_TR)
        self.up.CDS_SetAngle(8,635,100)
        self.up.CDS_SetAngle(9,330,100)
        self.up.CDS_SetAngle(10,774,speed1_TR)
        self.up.CDS_SetAngle(11,551,speed1_TR)
        self.up.CDS_SetAngle(12,395,speed2_TR)
        self.up.CDS_SetAngle(13,394,speed1_TR)
        self.up.CDS_SetAngle(14,610,100)
        self.up.CDS_SetAngle(15,278,100)
        self.up.CDS_SetAngle(16,511,speed1_TR)
        self.up.CDS_SetAngle(17,489,speed1_TR)
        self.up.CDS_SetAngle(18,392,speed2_TR)
        time.sleep(delay_TR)

        self.up.CDS_SetAngle(5,638,speed1_TR)
        self.up.CDS_SetAngle(6,290,speed2_TR)
        self.up.CDS_SetAngle(11,611,speed1_TR)
        self.up.CDS_SetAngle(12,320,speed2_TR)
        self.up.CDS_SetAngle(17,589,speed1_TR)
        self.up.CDS_SetAngle(18,317,speed2_TR)
        time.sleep(delay_TR+0.05)

        self.up.CDS_SetAngle(1,480,speed1_TR)
        self.up.CDS_SetAngle(2,519,speed1_TR)
        self.up.CDS_SetAngle(3,409,speed2_TR)
        self.up.CDS_SetAngle(4,437,speed1_TR)
        self.up.CDS_SetAngle(7,712,speed1_TR)
        self.up.CDS_SetAngle(8,535,speed1_TR)
        self.up.CDS_SetAngle(9,405,speed2_TR)
        self.up.CDS_SetAngle(10,574,speed1_TR)
        self.up.CDS_SetAngle(13,594,speed1_TR)
        self.up.CDS_SetAngle(14,510,speed1_TR)
        self.up.CDS_SetAngle(15,353,speed2_TR)
        self.up.CDS_SetAngle(16,311,speed1_TR)
        time.sleep(delay_TR)

        self.up.CDS_SetAngle(2,619,speed1_TR)
        self.up.CDS_SetAngle(3,334,speed2_TR)
        self.up.CDS_SetAngle(8,635,speed1_TR)
        self.up.CDS_SetAngle(9,330,speed2_TR)
        self.up.CDS_SetAngle(14,610,speed1_TR)
        self.up.CDS_SetAngle(15,278,speed2_TR)
        time.sleep(delay_TR+0.05)


    def BackForward(self):

        self.up.CDS_SetAngle(1,278,364)
        self.up.CDS_SetAngle(2,510,100)
        self.up.CDS_SetAngle(3,229,100)
        self.up.CDS_SetAngle(4,615,364)
        self.up.CDS_SetAngle(5,437,364)
        self.up.CDS_SetAngle(6,295,328)
        self.up.CDS_SetAngle(7,512,364)
        self.up.CDS_SetAngle(8,545,100)
        self.up.CDS_SetAngle(9,253,100)
        self.up.CDS_SetAngle(10,580,364)
        self.up.CDS_SetAngle(11,431,364)
        self.up.CDS_SetAngle(12,327,328)
        self.up.CDS_SetAngle(13,560,364)
        self.up.CDS_SetAngle(14,556,100)
        self.up.CDS_SetAngle(15,214,100)
        self.up.CDS_SetAngle(16,305,364)
        self.up.CDS_SetAngle(17,443,364)
        self.up.CDS_SetAngle(18,349,328)
        time.sleep(0.3)

        self.up.CDS_SetAngle(5,537,364)
        self.up.CDS_SetAngle(6,205,328)
        self.up.CDS_SetAngle(11,531,364)
        self.up.CDS_SetAngle(12,237,328)
        self.up.CDS_SetAngle(17,543,364)
        self.up.CDS_SetAngle(18,259,328)
        time.sleep(0.3)

        self.up.CDS_SetAngle(1,478,364)
        self.up.CDS_SetAngle(2,410,364)
        self.up.CDS_SetAngle(3,319,328)
        self.up.CDS_SetAngle(4,475,364)
        self.up.CDS_SetAngle(7,712,364)
        self.up.CDS_SetAngle(8,445,364)
        self.up.CDS_SetAngle(9,343,328)
        self.up.CDS_SetAngle(10,780,364)
        self.up.CDS_SetAngle(13,420,364)
        self.up.CDS_SetAngle(14,456,364)
        self.up.CDS_SetAngle(15,304,328)
        self.up.CDS_SetAngle(16,505,364)
        time.sleep(0.3)

        self.up.CDS_SetAngle(2,510,364)
        self.up.CDS_SetAngle(3,229,328)
        self.up.CDS_SetAngle(8,545,364)
        self.up.CDS_SetAngle(9,253,328)
        self.up.CDS_SetAngle(14,556,364)
        self.up.CDS_SetAngle(15,214,328)
        time.sleep(0.3)


    def Squat(self):

        ISC = self.IsStateChanged()

        self.up.CDS_SetAngle(1,472,512)
        self.up.CDS_SetAngle(2,430,512)
        self.up.CDS_SetAngle(3,119,512)
        self.up.CDS_SetAngle(4,530,512)
        self.up.CDS_SetAngle(5,488,512)
        self.up.CDS_SetAngle(6,140,512)
        self.up.CDS_SetAngle(7,593,512)
        self.up.CDS_SetAngle(8,446,512)
        self.up.CDS_SetAngle(9,185,512)
        self.up.CDS_SetAngle(10,627,512)
        self.up.CDS_SetAngle(11,414,512)
        self.up.CDS_SetAngle(12,122,512)
        self.up.CDS_SetAngle(13,490,512)
        self.up.CDS_SetAngle(14,426,512)
        self.up.CDS_SetAngle(15,95,512)
        self.up.CDS_SetAngle(16,429,512)
        self.up.CDS_SetAngle(17,429,512)
        self.up.CDS_SetAngle(18,131,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(1)


    def Standup(self):

        ISC = self.IsStateChanged()

        self.up.CDS_SetAngle(1,472,512)
        self.up.CDS_SetAngle(2,639,512)
        self.up.CDS_SetAngle(3,346,512)
        self.up.CDS_SetAngle(4,530,512)
        self.up.CDS_SetAngle(5,640,512)
        self.up.CDS_SetAngle(6,312,512)
        self.up.CDS_SetAngle(7,593,512)
        self.up.CDS_SetAngle(8,601,512)
        self.up.CDS_SetAngle(9,335,512)
        self.up.CDS_SetAngle(10,627,512)
        self.up.CDS_SetAngle(11,695,512)
        self.up.CDS_SetAngle(12,401,512)
        self.up.CDS_SetAngle(13,490,512)
        self.up.CDS_SetAngle(14,703,512)
        self.up.CDS_SetAngle(15,330,512)
        self.up.CDS_SetAngle(16,429,512)
        self.up.CDS_SetAngle(17,654,512)
        self.up.CDS_SetAngle(18,358,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(1)


    def BackSquat(self):

        ISC = self.IsStateChanged()

        self.up.CDS_SetAngle(1,390,512)
        self.up.CDS_SetAngle(2,539,512)
        self.up.CDS_SetAngle(3,320,512)
        self.up.CDS_SetAngle(4,450,512)
        self.up.CDS_SetAngle(5,627,512)
        self.up.CDS_SetAngle(6,278,512)
        self.up.CDS_SetAngle(7,592,512)
        self.up.CDS_SetAngle(8,668,512)
        self.up.CDS_SetAngle(9,402,512)
        self.up.CDS_SetAngle(10,715,512)
        self.up.CDS_SetAngle(11,551,512)
        self.up.CDS_SetAngle(12,324,512)
        self.up.CDS_SetAngle(13,585,512)
        self.up.CDS_SetAngle(14,602,512)
        self.up.CDS_SetAngle(15,282,512)
        self.up.CDS_SetAngle(16,429,512)
        self.up.CDS_SetAngle(17,678,512)
        self.up.CDS_SetAngle(18,356,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(1)


    def WaveHead(self):

        ISC = self.IsStateChanged()        
        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,512,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(0.3)
        self.up.CDS_SetAngle(19,462,512)
        self.up.CDS_SetAngle(20,562,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,512,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,562,512)
        self.up.CDS_SetAngle(20,562,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,512,512)
        time.sleep(0.3)

        if ISC == 1 :
            time.sleep(0.3)
        self.cyc +=  1

    def ShakeHead(self):
        self.cyc = 0
        ISC = self.IsStateChanged()
        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,580,512)
        time.sleep(0.3)
        while True:
            if self.cyc < 2:
                self.up.CDS_SetAngle(19,432,200)
                time.sleep(1)
                if ISC == 1 :
                    break
                self.up.CDS_SetAngle(19,592,200)
                time.sleep(1)
                if ISC == 1 :
                    break
                self.cyc += 1
            else:
                break
        self.up.CDS_SetAngle(19,512,200)
        self.up.CDS_SetAngle(20,512,512)
        time.sleep(0.5)


    def Nod(self):
        
        ISC = self.IsStateChanged()
        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,512,512)
        time.sleep(0.3)

        if ISC == 1 :
            time.sleep(0.3)
        self.up.CDS_SetAngle(19,462,512)
        self.up.CDS_SetAngle(20,562,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,462,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,562,512)
        self.up.CDS_SetAngle(20,562,512)
        time.sleep(0.3)

        self.up.CDS_SetAngle(19,512,512)
        self.up.CDS_SetAngle(20,462,512)
        time.sleep(0.3)
        if ISC == 1 :
            time.sleep(0.3)
        self.up.CDS_SetAngle(20,512,512)
        time.sleep(0.3)

    def Dance(self):

        ISC = self.IsStateChanged()

        self.up.CDS_SetAngle(1,441,512)
        self.up.CDS_SetAngle(2,647,512)
        self.up.CDS_SetAngle(3,358,512)
        self.up.CDS_SetAngle(4,553,512)
        self.up.CDS_SetAngle(5,447,512)
        self.up.CDS_SetAngle(6,651,512)
        self.up.CDS_SetAngle(7,574,512)
        self.up.CDS_SetAngle(8,666,512)
        self.up.CDS_SetAngle(9,327,512)
        self.up.CDS_SetAngle(10,616,512)
        self.up.CDS_SetAngle(11,435,512)
        self.up.CDS_SetAngle(12,642,512)
        self.up.CDS_SetAngle(13,501,512)
        self.up.CDS_SetAngle(14,658,512)
        self.up.CDS_SetAngle(15,289,512)
        self.up.CDS_SetAngle(16,488,512)
        self.up.CDS_SetAngle(17,463,512)
        self.up.CDS_SetAngle(18,637,512)
        time.sleep(0.5)                      #1,3,5蹲下，2，4，6抬起


        self.up.CDS_SetAngle(2,493,512)
        self.up.CDS_SetAngle(3,224,512)
        self.up.CDS_SetAngle(8,531,512)
        self.up.CDS_SetAngle(9,209,512)
        self.up.CDS_SetAngle(14,550,512)
        self.up.CDS_SetAngle(15,176,512)
        time.sleep(0.5)                     #1,3,5着地，2，4，6抬起

        self.up.CDS_SetAngle(2,647,512)
        self.up.CDS_SetAngle(3,358,512)
        self.up.CDS_SetAngle(8,666,512)
        self.up.CDS_SetAngle(9,327,512)
        self.up.CDS_SetAngle(14,658,512)
        self.up.CDS_SetAngle(15,289,512)
        time.sleep(0.5)                      #起立

        self.up.CDS_SetAngle(3,303,512)
        self.up.CDS_SetAngle(5,656,512)
        self.up.CDS_SetAngle(6,278,512)
        self.up.CDS_SetAngle(9,349,512)
        self.up.CDS_SetAngle(11,647,512)
        self.up.CDS_SetAngle(12,295,512)
        self.up.CDS_SetAngle(15,269,512)
        self.up.CDS_SetAngle(17,653,512)
        self.up.CDS_SetAngle(18,333,512)
        if ISC == 1 :
           time.sleep(0.3)
        time.sleep(0.6)                    #1,3,5抬起，2，4，6着地

        self.up.CDS_SetAngle(2,435,512)
        self.up.CDS_SetAngle(3,647,512)
        self.up.CDS_SetAngle(8,461,512)
        self.up.CDS_SetAngle(9,667,512)
        self.up.CDS_SetAngle(14,465,512)
        self.up.CDS_SetAngle(15,586,512)
        time.sleep(0.7)                      #1,3,5抬起，2，4，6蹲下

        self.up.CDS_SetAngle(5,525,512)
        self.up.CDS_SetAngle(6,194,512)
        self.up.CDS_SetAngle(11,519,512)
        self.up.CDS_SetAngle(12,229,512)
        self.up.CDS_SetAngle(17,509,512)
        self.up.CDS_SetAngle(18,197,512)
        time.sleep(0.3)                     #1,3,5抬起，2，4，6着地

        self.up.CDS_SetAngle(5,654,512)
        self.up.CDS_SetAngle(6,296,512)
        self.up.CDS_SetAngle(11,647,512)
        self.up.CDS_SetAngle(12,345,512)
        self.up.CDS_SetAngle(17,651,512)
        self.up.CDS_SetAngle(18,330,512)
        time.sleep(0.3)                     #起立

        self.up.CDS_SetAngle(2,648,512)
        self.up.CDS_SetAngle(3,303,512)
        self.up.CDS_SetAngle(6,278,512)
        self.up.CDS_SetAngle(8,667,512)
        self.up.CDS_SetAngle(9,349,512)
        self.up.CDS_SetAngle(12,295,512)
        self.up.CDS_SetAngle(14,640,512)
        self.up.CDS_SetAngle(15,269,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(0.7)


    def Play(self):
        self.cyc = 0      
        ISC = self.IsStateChanged()
        self.up.CDS_SetAngle(1,345,512)
        self.up.CDS_SetAngle(2,648,512)
        self.up.CDS_SetAngle(3,358,512)
        self.up.CDS_SetAngle(4,434,512)
        self.up.CDS_SetAngle(5,707,512)
        self.up.CDS_SetAngle(6,358,512)
        self.up.CDS_SetAngle(7,574,512)
        self.up.CDS_SetAngle(8,672,512)
        self.up.CDS_SetAngle(9,421,512)
        self.up.CDS_SetAngle(10,750,512)
        self.up.CDS_SetAngle(11,647,512)
        self.up.CDS_SetAngle(12,354,512)
        self.up.CDS_SetAngle(13,620,512)
        self.up.CDS_SetAngle(14,664,512)
        self.up.CDS_SetAngle(15,295,512)
        self.up.CDS_SetAngle(16,489,512)
        self.up.CDS_SetAngle(17,646,512)
        self.up.CDS_SetAngle(18,366,512)
        time.sleep(0.7)

        self.up.CDS_SetAngle(2,448,512)            #后四腿着地，前两腿抬起
        self.up.CDS_SetAngle(3,664,512)
        self.up.CDS_SetAngle(6,375,512)
        self.up.CDS_SetAngle(7,598,512)
        self.up.CDS_SetAngle(8,581,512)
        self.up.CDS_SetAngle(9,274,512)
        self.up.CDS_SetAngle(11,480,512)
        self.up.CDS_SetAngle(12,694,512)
        self.up.CDS_SetAngle(14,690,512)
        self.up.CDS_SetAngle(15,354,512)
        self.up.CDS_SetAngle(16,429,512)
        self.up.CDS_SetAngle(17,550,512)
        self.up.CDS_SetAngle(18,244,512)
        time.sleep(0.7)

        while True:

            if self.cyc < 4:
                self.up.CDS_SetAngle(2,401,800)          #前右腿落下，前左腿抬起
                self.up.CDS_SetAngle(3,784,800)
                self.up.CDS_SetAngle(11,613,800)
                self.up.CDS_SetAngle(12,531,800)
                time.sleep(0.3)

                self.up.CDS_SetAngle(2,611,800)          #前左腿落下，前右腿抬起
                self.up.CDS_SetAngle(3,556,800)
                self.up.CDS_SetAngle(11,409,800)
                self.up.CDS_SetAngle(12,769,800)

                time.sleep(0.3)
                if ISC == 1 :
                    break
                self.cyc += 1
            else:
                break

        self.up.CDS_SetAngle(2,648,512)                  #后四腿着地，前两腿前迈
        self.up.CDS_SetAngle(3,358,512)
        self.up.CDS_SetAngle(8,672,512)
        self.up.CDS_SetAngle(9,421,512)
        self.up.CDS_SetAngle(11,647,512)
        self.up.CDS_SetAngle(12,354,512)
        self.up.CDS_SetAngle(17,646,512)
        self.up.CDS_SetAngle(18,366,512)
        if ISC == 1 :
            time.sleep(0.3)
        time.sleep(0.5)
        
    def start(self):
        j=0
        bFirst = 0
        print('start')
        #self.ready()
        self.Standup()
        while True:
            robot_state_ISC = self.GetState()
            ISC = self.IsStateChanged()
            self.GetState()         
            if robot_state_ISC == 1:  # 无障碍
                if self.forward_flag == 1:
                    self.GoForward()
                else:
                    if ISC == 0:
                        j = j + 1
                        j %= 15
                        if j > 13:
                            self.forward_flag = 1
                    self.Standup()

            if robot_state_ISC == 2:  # 左侧障碍
                if ISC == 1:
                    self.BackForward()
                self.TurnRight()

            if robot_state_ISC == 3:  # 右侧障碍
                if ISC == 1:
                    self.BackForward()
                self.TurnLeft()

            if robot_state_ISC == 4:  # 前方障碍
                self.BackForward()

            if robot_state_ISC == 5:  # zad检测到障碍——io没有检测到障碍
                self.WaveHead()
                self.BackForward()
                self.Squat()
                self.Standup()

            if robot_state_ISC == 6:  # ad检测到障碍很近——io没有检测到
                self.BackForward()
                if bFirst == 0:
                    self.Nod()
                    self.Dance()
                    bFirst =  1
                else:
                    self.Standup()
                    self.Play()
                    bFirst = 0

if __name__ == '__main__':
   liuzu = LIUZU()
   liuzu.start()
  




 




















   
   
   