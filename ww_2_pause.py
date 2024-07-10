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


servo_r = 532 + 300    # #6.#4=+90du, #7.#5=-90du.
servo_l = 532 - 300
servo_speed = 800
up.CDS_SetMode(4,up.CDS_MODE_SERVO)
up.CDS_SetMode(5,up.CDS_MODE_SERVO)
up.CDS_SetMode(6,up.CDS_MODE_SERVO)
up.CDS_SetMode(7,up.CDS_MODE_SERVO)
# 
controller.up.CDS_SetAngle(4, servo_r, servo_speed)
controller.up.CDS_SetAngle(5, servo_l, servo_speed)
controller.up.CDS_SetAngle(6, servo_r , servo_speed)
controller.up.CDS_SetAngle(7, servo_l , servo_speed)

up.CDS_SetSpeed(1, 0)
up.CDS_SetSpeed(2, 0)


# up.CDS_SetSpeed(1, 0)
# up.CDS_SetSpeed(2, 0)
# time.sleep(0.5)
# 
# controller.up.CDS_SetAngle(6, 532-45, servo_speed)
# controller.up.CDS_SetAngle(7, 532 + 55, servo_speed)
