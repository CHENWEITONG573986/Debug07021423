'''
  Note: test duoji #4,#5,#6,#7.
  2023.3.17.OK 
'''
# ====================================================================================

from up_controller import UpController
import uptech
import time
import threading
controller = UpController()
up = uptech.UpTech()
up.CDS_Open()
up.LCD_Open(2)

arm46_angle90 = 532 + 300 #number of arm (4 and 6) ---angle 90°
arm57_angle90 = 532 - 300 #number of arm (5 and 7) ---angle 90°

up.CDS_SetSpeed(1, 800)
up.CDS_SetSpeed(2, 800)

servo_speed = 800
up.CDS_SetMode(4,up.CDS_MODE_SERVO)
up.CDS_SetMode(5,up.CDS_MODE_SERVO)
up.CDS_SetMode(6,up.CDS_MODE_SERVO)
up.CDS_SetMode(7,up.CDS_MODE_SERVO)
# turn
controller.up.CDS_SetAngle(4, arm46_angle90, servo_speed)
controller.up.CDS_SetAngle(5, arm57_angle90, servo_speed)
controller.up.CDS_SetAngle(6, arm46_angle90, servo_speed)
controller.up.CDS_SetAngle(7, arm57_angle90, servo_speed)
time.sleep(1.0)
# 重置角度为90°
controller.up.CDS_SetAngle(4, 532, servo_speed)
controller.up.CDS_SetAngle(5, 532, servo_speed)
controller.up.CDS_SetAngle(6, 560, servo_speed)
controller.up.CDS_SetAngle(7, 498, servo_speed)

up.CDS_SetSpeed(1, 0)
up.CDS_SetSpeed(2, 0)


# up.CDS_SetSpeed(1, 0)
# up.CDS_SetSpeed(2, 0)
# time.sleep(0.5)
# 
# controller.up.CDS_SetAngle(6, 532-45, servo_speed)
# controller.up.CDS_SetAngle(7, 532 + 55, servo_speed)
