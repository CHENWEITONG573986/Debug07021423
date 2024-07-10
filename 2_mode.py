'''
  Note: test duoji #4,#5,#6,#7.
  2023.3.17.OK 
'''
# ====================================================================================

from up_controller import UpController
import uptech
import time
import threading
servo_speed = 800
turn_speed = 700 
speed = -900
tx_speed = 450
speed = 400     #walking slow=400,quick = 520,middle=460
# speedl = -650
speedl = 400
# speedl = 600
# 512 576
crush_speed = 650
# SPEED = 256
controller = UpController()
up = uptech.UpTech()
up.CDS_Open()
up.LCD_Open(2)
open_flag = up.ADC_IO_Open()

io_data = []
def get_io_vaule():
    while True:
        io_all_input = up.ADC_IO_GetAllInputLevel()
        # print("io_vaule = {}".format(io_all_input))
        io_array = '{:08b}'.format(io_all_input)
        io_data.clear()
        for index, value in enumerate(io_array):
            io_value = (int)(value)
            io_data.insert(0, io_value)
            
            
edge_thread = threading.Thread(name = "edge_detect_thread",target=get_io_vaule)
edge_thread.setDaemon(True)
edge_thread.start()


servo_r = 532 + 300    # #6.#4=+90du, #7.#5=-90du.
servo_l = 532 - 300 
# up.CDS_SetSpeed(1, 500)
# up.CDS_SetSpeed(2, -500)
up.CDS_SetSpeed(1, 0)
up.CDS_SetSpeed(2, 0)
up.CDS_SetMode(4,up.CDS_MODE_SERVO)
up.CDS_SetMode(5,up.CDS_MODE_SERVO)
up.CDS_SetMode(6,up.CDS_MODE_SERVO)
up.CDS_SetMode(7,up.CDS_MODE_SERVO)
# 
controller.up.CDS_SetAngle(4, servo_r+20 ,servo_speed)
controller.up.CDS_SetAngle(5, servo_l-20, servo_speed)
controller.up.CDS_SetAngle(6, servo_r+20, servo_speed)
controller.up.CDS_SetAngle(7, servo_l-20, servo_speed)

# up.CDS_SetSpeed(1, -(speedl+100))
# up.CDS_SetSpeed(2, speedl)
# time.sleep(0.4)
# up.CDS_SetSpeed(1, -(speedl+50))
# up.CDS_SetSpeed(2, -(speedl+50))
# while True:
#     if not io_data[7] and not io_data[6]:
#         break
# up.CDS_SetSpeed(1, 0)
# up.CDS_SetSpeed(2, 0)


# up.CDS_SetSpeed(1, 0)
# up.CDS_SetSpeed(2, -0)
# up.CDS_SetSpeed(1, 300)
# up.CDS_SetSpeed(2, -300)
# time.sleep(0.6)
# up.CDS_SetSpeed(1, 0)
# up.CDS_SetSpeed(2, 0)
def st():
    # down front zhuazi
    up.CDS_SetSpeed(1, 700)
    up.CDS_SetSpeed(2, -700)
    
    controller.up.CDS_SetAngle(6, 532-100, servo_speed)
    controller.up.CDS_SetAngle(7, 532+100, servo_speed)#850 

    time.sleep(0.6)

    # up front zuazi
    controller.up.CDS_SetAngle(6, servo_r, servo_speed)
    controller.up.CDS_SetAngle(7, servo_l, servo_speed)

    # time.sleep(0.4)

    # up.CDS_SetSpeed(1, 0)
    # up.CDS_SetSpeed(2, 0)
    #  2
    time.sleep(0.2)
    # ---------------------------------------
        
    # down back zhuazi 
    controller.up.CDS_SetAngle(4, 532-150, servo_speed)
    controller.up.CDS_SetAngle(5, 532+150, servo_speed)

    time.sleep(0.9)
    #up.CDS_SetSpeed(1, speed)
    #up.CDS_SetSpeed(2, -speed)
    #time.sleep(0.3)
    
    # up back zhuazi
    controller.up.CDS_SetAngle(4, servo_r, servo_speed)
    controller.up.CDS_SetAngle(5, servo_l, servo_speed)

    time.sleep(0.8)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)

    # reset all
    controller.up.CDS_SetAngle(4, servo_r, servo_speed)
    controller.up.CDS_SetAngle(5, servo_l, servo_speed)
    controller.up.CDS_SetAngle(6, servo_r, servo_speed)
    controller.up.CDS_SetAngle(7, servo_l, servo_speed)
    make_a_turn(1,0.9)
    time.sleep(0.2)
    up.CDS_SetSpeed(1, 700)
    up.CDS_SetSpeed(2, -700)
    time.sleep(0.3)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)
    time.sleep(0.2)
# ====================================================================================
# 1---#6,#7 duoji
def make_a_turn(direction = 1, times = 1.0):
    '''
    control the car to make a turn
    :param direction:1 means right, -1 means left, default right
    :param times:1 means 90 degrees, 2 means 180 degrees, default 90 degrees
    :return: no return
    '''
    up.CDS_SetSpeed(1, turn_speed * direction)
    up.CDS_SetSpeed(2, turn_speed * direction)
    time.sleep(0.55 * times)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)
    time.sleep(0.1)

def move(direction = 1, times = 1):
    '''
    control the car to move
    :param direction:1 means forward, -1 means backward, default forward
    :param times:1 means 1s, default 1s
    :return: no return
    '''
    # move time default 1s
    up.CDS_SetSpeed(1, tx_speed * direction)
    up.CDS_SetSpeed(2, -tx_speed * direction)
    time.sleep(times+0.3)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)
#make_a_turn(1,0.8)#90du
# make_a_turn(1, 0.6)#50du
# move(-1,1)
#st()
# up.CDS_SetSpeed(1, -1000)
# up.CDS_SetSpeed(2, -1000)
#time.sleep(2.0)
# up.CDS_SetSpeed(1, -1000)
# up.CDS_SetSpeed(2, -1000)
# time.sleep(1.5)
#up.CDS_SetSpeed(1, 0)
#up.CDS_SetSpeed(2, 0)

