'''
  Ver:  xiu-gai ff_12_fs+bs01.py
  Date: 2023-06-12-----
  ccd is testing......
'''

from up_controller import UpController
import uptech
import time
import threading
import cv2
import apriltag


up = uptech.UpTech()
up.CDS_Open()
up.LCD_Open(2)
open_flag = up.ADC_IO_Open()
controller = UpController()

thresh = 26    #yu zhi

servo_speed = 1000
#### shexiangtou id 

my_id = 2
enemy = 1

table_flag = 1
count_time = 0

tagid_enemy = 0
tagid_enemy_1 = 0
down_tagid_enemy = 0

turn_tangle = 0.8
# tx_speed = -660
tx_speed = 450
# st_speed = -900
st_speed = 680
# st_speed = 700

turn_speed = 600      # down plat turn spwwd to search plat.

# speed = -570
speed = 512     #walking slow=400,quick = 520,middle=460
# speedl = -650
speedl = 450
# speedl = 600
# 512 576
crush_speed = 650
#crush_speed = 770
# 800 700
# 768

servo_r = 532 + 300    # #6.#4=+90du, #7.#5=-90du.
servo_l = 532 - 300 

# #7=left front #6=right front #4=left bake #5=right bake 
servo_r_o = 532 - 200   #-200 -> -60du zhicheng(#6,#4)
servo_l_o = 532 + 200   #+200 -> -60du zhicheng(#7,#5) #20230607


io_data = []

flag = False

def get_io_value():
    global flag
    while True:
        adc_data = up.ADC_Get_All_Channle()
        # print("adc0,adc1",adc_data[0],adc_data[1])
        #taixia:   [0]<=1500,[1]<=900
        if adc_data[0 ] < 2100 or adc_data[1] < 1300 :
            flag = False
        #elif adc_data[0] - adc_data[1] <= 600:
        #    flag = 32
        #elif adc_data[0] - adc_data[1] >= 1300:
        #    flag = 10
        else :
            flag = True
        
        io_all_input = up.ADC_IO_GetAllInputLevel()
        # print("io_vaule = {}".format(io_all_input))
        io_array = '{:08b}'.format(io_all_input)
        io_data.clear()
        for index, value in enumerate(io_array):
            io_value = (int)(value)
            io_data.insert(0, io_value)
        #print('---', flag, adc_data[0], adc_data[1])

tag_id = -1
camera_id = 0
def get_qr_value():
    global camera_id
    cap = cv2.VideoCapture(camera_id)
    at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
    global tag_id
    w = 640#640
    h = 480#480
#     weight =320#320  #520
    weight = 320
    cap.set(3,w)
    cap.set(4,h)

    cup_w = (int)((w - weight) / 2)
    cup_h = (int)((h - weight) / 2) + 50   #   bian jie she zhi
    
    while True:
        try:
            ret, frame = cap.read()
            frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
            camera_id = 0
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tags = at_detector.detect(gray)
        
            tag_id = tags[0].tag_id if len(tags) else -1
#             cv2.imshow('video', frame)
            c = cv2.waitKey(1) & 0xff
            if c == 27:
                cap.release()
                break
        
       
        except Exception as e:
            print("Exception:", e)
            print(camera_id)
            # 在此处添加重新启动线程的代码
            cap.release()
            cap = cv2.VideoCapture(camera_id)
            camera_id = camera_id + 1
            if camera_id >2:
                camera_id = 0
            at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
            continue
    cap.release()
    cv2.destroyAllWindows()
#         except Exception as ee:
#             pass
#             print("Errot: ", ee)
        #cv2.imshow('video', frame)
        #c = cv2.waitKey(1) & 0xff
        #if c == 27:
            #cap.release()
            #break
    #cap.release()
    #cv2.destroyAllWindows()
#             
state_flag = True
def detect_state():
    global state_flag
    while True:
        if not state_flag:
            time.sleep(1)
            time.sleep(0.5)
            state_flag = True


qr_thread = threading.Thread(name = "qr_detect_thread",target=get_qr_value)
qr_thread.setDaemon(True)
qr_thread.start()
# xiu gai13.55
# thread1 --- check huidu to change 'flag'.
edge_thread = threading.Thread(name = "edge_detect_thread",target=get_io_value)
edge_thread.setDaemon(True)
edge_thread.start()

# ???
state_thread = threading.Thread(name = "detect_state_thread",target=detect_state)
state_thread.setDaemon(True)
state_thread.start()


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
    make_a_turn(1,1.0)
    time.sleep(0.2)
    while True:
        if io_data[0] or io_data[2]:
            up.CDS_SetSpeed(1, -700)
            up.CDS_SetSpeed(2, 700)
            time.sleep(0.3)
            break
        else:
            up.CDS_SetSpeed(1, 700)
            up.CDS_SetSpeed(2, -700)
            time.sleep(0.5)
            break
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)
    time.sleep(0.2)

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
    time.sleep(times)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)


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


def all_reset():
    controller.up.CDS_SetAngle(4, servo_r_o, servo_speed)
    controller.up.CDS_SetAngle(5, servo_l_o, servo_speed)
    controller.up.CDS_SetAngle(6, servo_r_o, servo_speed)
    controller.up.CDS_SetAngle(7, servo_l_o, servo_speed)

    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)


if __name__ == '__main__':
    # Reset to up: #4.#5.#6.#7
    # stop motor #1(left), #2(right).
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)

    # Reset duoji #4,#5,#6,#7.
    controller.up.CDS_SetAngle(4, servo_r, servo_speed)
    controller.up.CDS_SetAngle(5, servo_l, servo_speed)
    controller.up.CDS_SetAngle(6, servo_r, servo_speed)
    controller.up.CDS_SetAngle(7, servo_l, servo_speed)
    
    # =====================================================
    
    time.sleep(0.5)
    print('step1..... waiting [4]and[5] to start !')
    
    # Soft Start!
    while True:
#         
        if not io_data[4] or not io_data[5]:
#             
            break
      
    up.CDS_SetSpeed(1, speed)
    up.CDS_SetSpeed(2, -speed)
    time.sleep(0.6)

#     up.CDS_SetSpeed(1, 80) 
#     up.CDS_SetSpeed(2, -80)     # slow move forwerd.
#     
    print("step2.....Go!")
    
    while True:
        try:
            ##print("flag:",flag,'-----',io_data[0],io_data[2])
            
            # flag = True (on-plat)
            #判断是否在台上
            if flag:                #flag tai up tai down
                table_flag = 0
                # print("taishang")
#                 print("if",end=".")
               # print(io_data)
                #放下前舵机
                controller.up.CDS_SetAngle(6, 500, servo_speed)
                controller.up.CDS_SetAngle(7, 575, servo_speed)# 20230607
                #debug---20230607
#                 up.CDS_SetSpeed(1, speed)
#                 up.CDS_SetSpeed(2, -speed)
                
                #如果识别到前方为敌人或0
                if tag_id == enemy or tag_id == 0 :
                    tagid_enemy_1 = 0
                    tagid_enemy = tagid_enemy + 1
                    print("tagid=enemy_1: ",tag_id)
                    #冲
                    up.CDS_SetSpeed(1, crush_speed)
                    up.CDS_SetSpeed(2, -crush_speed)
#                     if io_data[0] or io_data[2]:
                    while True:
                        if io_data[0] or io_data[2]:
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                            time.sleep(0.2)
                            
                            if tagid_enemy == 2:
                                print("enemy == 3")
                                if io_data[0]:
                                    up.CDS_SetSpeed(1, -300)
                                    up.CDS_SetSpeed(2, -300)
                                    time.sleep(0.4)
                                if io_data[2]:
                                    up.CDS_SetSpeed(1, 300)
                                    up.CDS_SetSpeed(2, 300)
                                    time.sleep(0.4)
                            break
                        if io_data[6] and io_data[7]:
                            up.CDS_SetSpeed(1, 400)
                            up.CDS_SetSpeed(2, -400)
                            break
                    time.sleep(0.2)
                    up.CDS_SetSpeed(1, 300)
                    up.CDS_SetSpeed(2, -300)
                    time.sleep(0.2)
                    if tagid_enemy == 2:
                        print("add time")
                        tagid_enemy = 0
                        time.sleep(1.2)
                    up.CDS_SetSpeed(1, -400)
                    up.CDS_SetSpeed(2, 400)
                    time.sleep(0.4)
                    up.CDS_SetSpeed(1, 0)
                    up.CDS_SetSpeed(2, 0)
                    

#////////////////////////////////
                #如果前方为我方
                elif tag_id == my_id:
                    tagid_enemy = 0
                    tagid_enemy_1 = 0
                    print("tagid = my_id",tag_id)
#                     controller.up.CDS_SetAngle(6, servo_r, servo_speed)
#                     controller.up.CDS_SetAngle(7, servo_l, servo_speed)
#                     
                    up.CDS_SetSpeed(1, -speedl)
                    up.CDS_SetSpeed(2, speedl)
                    time.sleep(0.4)
                    up.CDS_SetSpeed(1, 0)
                    up.CDS_SetSpeed(2, 0)
                    make_a_turn(1,1.2)
                    time.sleep(0.6)
                #后方到边缘
                elif io_data[0] or io_data[2]:#倒退
                    tagid_enemy = 0
                    tagid_enemy_1 = 0
                    up.CDS_SetSpeed(1, 0)
                    up.CDS_SetSpeed(2, 0)     #wu xu ting zhi
                    time.sleep(0.2)
                    #右方为障碍物
                    if not io_data[4]:
                        print("down--right")
                        up.CDS_SetSpeed(1, -speedl)
                        up.CDS_SetSpeed(2, speedl)
                        time.sleep(0.6)

                        if io_data[1] or io_data[3]:
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
    
                        
                        up.CDS_SetSpeed(1, (speedl))
                        up.CDS_SetSpeed(2, (speedl))
                        time.sleep(0.8)
                        # start_time = time.time()
                        # while True:
                        #     current_time = time.time()
                        #     if not io_data[6] or (current_time - start_time) >= 3:
                        #         break
                        
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        if io_data[0] and not io_data[1]:
                            make_a_turn(-1,0.3)
                            time.sleep(0.2)
                        elif not io_data[0] and io_data[1]:
                            make_a_turn(1,0.3)
                            time.sleep(0.2)
                        else:
                            time.sleep(0.2)
                        
                    #左边为障碍物
                    elif not io_data[5]:
                        print("down--left")
                        up.CDS_SetSpeed(1, -speedl)
                        up.CDS_SetSpeed(2, speedl)
                        time.sleep(0.6)

                        if io_data[1] or io_data[3]:
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                        up.CDS_SetSpeed(1, -(speedl))
                        up.CDS_SetSpeed(2, -(speedl))
                        time.sleep(0.8)
                        # start_time = time.time()
                        # while True:
                        #     current_time = time.time()
                        #     if not io_data[6] or (current_time - start_time) >= 3:
                        #         break
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        if io_data[3] and not io_data[2]:
                            make_a_turn(-1,0.3)
                            time.sleep(0.2)
                        elif not io_data[3] and io_data[2]:
                            make_a_turn(1,0.3)
                            time.sleep(0.2)
                        else:
                            time.sleep(0.2)
                    elif not io_data[4] or not io_data[5]:
                        print('right or left')
                        if not io_data[4]:
                            up.CDS_SetSpeed(1, -speedl)
                            up.CDS_SetSpeed(2, (speedl+100))
                            time.sleep(0.4)
                            up.CDS_SetSpeed(1, (speedl+50))
                            up.CDS_SetSpeed(2, (speedl+50))
                        else :
                            up.CDS_SetSpeed(1, -(speedl+100))
                            up.CDS_SetSpeed(2, speedl)
                            time.sleep(0.4)
                            up.CDS_SetSpeed(1, -(speedl))
                            up.CDS_SetSpeed(2, -(speedl))
                            time.sleep(0.8)
                        # start_time = time.time()
                        # while True:
                        #     current_time = time.time()
                        #     if not io_data[6] or (current_time - start_time) >= 3:
                        #         break
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        time.sleep(0.2)
                    #前方为障碍物
                    elif not io_data[6] and not io_data[7]:
                        time.sleep(0.5)
                        #我方箱子
                        if tag_id == my_id:
                            down_tagid_enemy = 0
                            print("down_67_my")
                            up.CDS_SetSpeed(1, -speedl)
                            up.CDS_SetSpeed(2, speedl)
                            time.sleep(0.4)
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                            make_a_turn(1,turn_tangle+0.4)
                            time.sleep(0.4)
                        #敌方或中立箱子
                        if tag_id == enemy or tag_id == 0:
                            down_tagid_enemy = down_tagid_enemy + 1 
                            print("down_67  enemy")
                            if down_tagid_enemy == 2:
                                print("down_tagid_enemy == 3")
                                down_tagid_enemy = 0
                                time.sleep(0.4)
                                if io_data[0]:
                                    up.CDS_SetSpeed(1, -300)
                                    up.CDS_SetSpeed(2, -300)
                                    time.sleep(0.4)
                                if io_data[2]:
                                    up.CDS_SetSpeed(1, 300)
                                    up.CDS_SetSpeed(2, 300)
                                    time.sleep(0.4)
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                            time.sleep(0.2)   
                            up.CDS_SetSpeed(1, 400)
                            up.CDS_SetSpeed(2, -400)
                            time.sleep(0.6)
                                
                    else:
                        down_tagid_enemy = 0
                        print("down")
                        up.CDS_SetSpeed(1, -speedl)
                        up.CDS_SetSpeed(2, speedl)#20230525
                        time.sleep(0.6)
                        
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        time.sleep(0.0)
                        
                        if io_data[1]:
                                up.CDS_SetSpeed(1, -speedl)
                                up.CDS_SetSpeed(2, -speedl)
                        elif io_data[3]:
                                up.CDS_SetSpeed(1, speedl)
                                up.CDS_SetSpeed(2, speedl)
                        else :
                            up.CDS_SetSpeed(1, speedl)
                            up.CDS_SetSpeed(2, speedl)
                            
                        time.sleep(0.4)    # xuan zhuan jia shi
                    
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        
                        time.sleep(0.1)    
                        
                #后方为边缘
                elif io_data[1] or io_data[3]:#up jiaoluo
                    tagid_enemy = 0
                    tagid_enemy_1 =0
                    #右边为障碍物
                    if not io_data[4]:
                        print("up--right")
                        up.CDS_SetSpeed(1, speedl)
                        up.CDS_SetSpeed(2, -speedl)
                        time.sleep(0.6)
                        #前方为障碍物
                        if io_data[0] or io_data[2]:
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                        time.sleep(0.4)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)

                        time.sleep(0.6)
                        
                        make_a_turn(1,turn_tangle)
                        time.sleep(0.0)
                        
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        
                        if io_data[2] and not io_data[3]:
                            make_a_turn(-1,0.25)
                            time.sleep(0.2)
                        elif not io_data[2] and io_data[3]:
                            make_a_turn(1,0.25)
                            time.sleep(0.2)
                        else:
                            time.sleep(0.2)
                    elif not io_data[5]:
                        print("up--left")
                        up.CDS_SetSpeed(1, speedl)
                        up.CDS_SetSpeed(2, -speedl)
                        time.sleep(0.6)
                        if io_data[0] or io_data[2]:
                            up.CDS_SetSpeed(1, 0)
                            up.CDS_SetSpeed(2, 0)
                        time.sleep(0.4)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)

                        time.sleep(0.6)
                        
                        make_a_turn(-1,turn_tangle)
                        if io_data[0] and not io_data[1]:
                            make_a_turn(-1,0.25)
                            time.sleep(0.2)
                        elif not io_data[0] and io_data[1]:
                            make_a_turn(1,0.25)
                            time.sleep(0.2)
                        else:
                            time.sleep(0.2)

                    else:
                        print("up")
                        up.CDS_SetSpeed(1, speedl)
                        up.CDS_SetSpeed(2, -speedl)#20230525
                        time.sleep(0.6)
                        
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        time.sleep(0.0)
                        
                        if io_data[0]:
                                up.CDS_SetSpeed(1, -speedl)
                                up.CDS_SetSpeed(2, -speedl)
                        elif io_data[2]:
                                up.CDS_SetSpeed(1, speedl)
                                up.CDS_SetSpeed(2, speedl)
                        else :
                            up.CDS_SetSpeed(1, speedl)
                            up.CDS_SetSpeed(2, speedl)
                            
                        time.sleep(0.5)    # xuan zhuan jia shi
                    
                        up.CDS_SetSpeed(1, speed)
                        up.CDS_SetSpeed(2, -speed)
                        
                        time.sleep(0.1)   
 #555555555555555555                 
                elif not io_data[4] and io_data[6] and io_data[7] :
                    tagid_enemy = 0
                    tagid_enemy_1 = 0
      #              if not io_data[4] and io_data[6] and io_data[7] and state_flag:
                    print('---right')
                    up.CDS_SetSpeed(1, -speedl)
                    up.CDS_SetSpeed(2, (speedl))
                    time.sleep(0.8)
                    up.CDS_SetSpeed(1, (speedl+50))
                    up.CDS_SetSpeed(2, (speedl+50))
                    time.sleep(0.8)
                    # start_time = time.time()
                    # while True:
                    #     current_time = time.time()
                    #     if not io_data[6] or (current_time - start_time) >= 3:
                    #         break
                    up.CDS_SetSpeed(1, 0)
                    up.CDS_SetSpeed(2, 0)
                    time.sleep(0.2)
                elif not io_data[5] and io_data[6] and io_data[7] :
                    tagid_enemy = 0
                    tagid_enemy_1 = 0
                    print('---left')
                    up.CDS_SetSpeed(1, -(speedl))
                    up.CDS_SetSpeed(2, speedl)
                    time.sleep(0.)
                    up.CDS_SetSpeed(1, -(speedl))
                    up.CDS_SetSpeed(2, -(speedl))
                    time.sleep(0.8)
                    # start_time = time.time()
                    # while True:
                    #     current_time = time.time()
                    #     if not io_data[6] or (current_time - start_time) >= 3:
                    #         break
                    up.CDS_SetSpeed(1, 0)
                    up.CDS_SetSpeed(2, 0)
                    time.sleep(0.2)
                elif not io_data[6] and not io_data[7]:    #er-wei-ma jiance
                    print('io_6-io_7')
                    time.sleep(0.5)
                    tagid_enemy = 0
                    if tag_id == my_id:
                        print("my_id=my_id!!!: ",tag_id)
                        up.CDS_SetSpeed(1, -speedl)      #back
                        up.CDS_SetSpeed(2, speedl)
                        time.sleep(0.5)
                            ##print("tagid: ",tag_id)
                        if io_data[1] :
                            up.CDS_SetSpeed(1, -500)
                            up.CDS_SetSpeed(2, -500)
                            time.sleep(0.7)
                        elif io_data[3]:
                            up.CDS_SetSpeed(1, 500)
                            up.CDS_SetSpeed(2, 500)
                            time.sleep(0.7)
                        time.sleep(0.6)
                            
                        state_flag = False
                            
                        make_a_turn(direction = 1,times = 0.8) #1.1
                            
                        time.sleep(0.1)
                        up.CDS_SetSpeed(1, speed)
                        up.CDS_SetSpeed(2, -speed)
#                             
#                         elif tag_id == 1:
#                             print("tagid=1: ",tag_id)
#                             up.CDS_SetSpeed(1, crush_speed)
#                             up.CDS_SetSpeed(2, -crush_speed)
                    elif tag_id == enemy or tag_id == 0 :
                        tagid_enemy_1 = tagid_enemy_1 + 1
                        print("tagid=ennmy_2: ",tag_id)
                        up.CDS_SetSpeed(1, crush_speed)
                        up.CDS_SetSpeed(2, -crush_speed)
    #                     if io_data[0] or io_data[2]:
                        while True:
                            if io_data[0] or io_data[2]:
                                up.CDS_SetSpeed(1, 0)
                                up.CDS_SetSpeed(2, 0)
                                time.sleep(0.2)
                                if tagid_enemy_1 == 3:
                                    print("enemy == 3")
                                    if io_data[0]:
                                        up.CDS_SetSpeed(1, -300)
                                        up.CDS_SetSpeed(2, -300)
                                        time.sleep(0.4)
                                    if io_data[2]:
                                        up.CDS_SetSpeed(1, 300)
                                        up.CDS_SetSpeed(2, 300)
                                        time.sleep(0.4)
                                break
                            if io_data[6] and io_data[7]:
                                up.CDS_SetSpeed(1, 400)
                                up.CDS_SetSpeed(2, -400)
                                break
                        time.sleep(0.2)
                        up.CDS_SetSpeed(1, 300)
                        up.CDS_SetSpeed(2, -300)
                        time.sleep(0.2)
                        if tagid_enemy_1 == 3:
                            print("add time")
                            tagid_enemy_1 = 0
                            time.sleep(1.0)
                        up.CDS_SetSpeed(1, -400)
                        up.CDS_SetSpeed(2, 400)
                        time.sleep(0.4)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        
                    elif tag_id == -1:
                        print("tagid=-1: ",tag_id)
                        
                        up.CDS_SetSpeed(1, crush_speed)
                        up.CDS_SetSpeed(2, -crush_speed)
                        start_time = time.time()
                        while True:
                            current_time = time.time()
                            if (current_time - start_time) >=2:
                                up.CDS_SetSpeed(1, 750)
                                up.CDS_SetSpeed(2, -750)
                            if io_data[6] or io_data[7] or io_data[2] or io_data[0]:
                                break
                        up.CDS_SetSpeed(1, -500)
                        up.CDS_SetSpeed(2, 500)
                        time.sleep(0.8)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        
                    else:
                        print("tagid_else: ",tag_id)
                            
                        time.sleep(0.1)
                        up.CDS_SetSpeed(1, crush_speed)
                        up.CDS_SetSpeed(2, -crush_speed)
#                             print("tagid: ",tag_id)
#                             time.sleep(0.01)
                else:
                    tagid_enemy = 0
                    tagid_enemy_1 = 0
#                     print("other")
                    up.CDS_SetSpeed(1, crush_speed)
                    up.CDS_SetSpeed(2, -crush_speed)
            # flag = False (down-plat)
            # elif flag == 10:
            #     print("10")
            #     up.CDS_SetSpeed(1, 1000)
            #     up.CDS_SetSpeed(2, -1000)
            #     time.sleep(1.0)
            #     up.CDS_SetSpeed(1, 1000)
            #     up.CDS_SetSpeed(2, 1000)
            #     time.sleep(1.5)
            #     up.CDS_SetSpeed(1, 0)
            #     up.CDS_SetSpeed(2, 0)
            # elif flag == 32:
            #     print("32")
            #     up.CDS_SetSpeed(1, -1000)
            #     up.CDS_SetSpeed(2, -1000)
            #     time.sleep(1.0)
            #     up.CDS_SetSpeed(1, -1000)
            #     up.CDS_SetSpeed(2, -1000)
            #     time.sleep(1.5)
            #     up.CDS_SetSpeed(1, 0)
            #     up.CDS_SetSpeed(2, 0)
            else:
                table_flag = 1
                # print("taixia ")
                # front zhuazi up (90du)
                
                controller.up.CDS_SetAngle(6, servo_r, servo_speed)
                controller.up.CDS_SetAngle(7, servo_l, servo_speed)
                
                # find plat.   --- [6]low = 0(led-on), [7]hight = 1(led-off),  
                if not io_data[6] and io_data[7] and io_data[4] and io_data[5]:
                    print("T:",io_data[6],io_data[7],io_data[4],io_data[5])
                    # go-up to plat.
                    #time.sleep(0.6)
#                     move(1,0.8)
                    move(1,1)    #shuo duan time
                    print("stzhengzaizhixin")
                    st()
                    
                    #time.sleep(1.4)
                    
                    if flag:
                        up.CDS_SetSpeed(1, speed)
                        up.CDS_SetSpeed(2, -speed)
                    #all_reset()
                    
        
                # face weilang, then turn right 90du.
                elif (not io_data[6] and not io_data[7]) and (io_data[4] and io_data[5]):     #zhong,jian
                    print("weilan")
                    time.sleep(0.2)
                    # 1=turn right, 2=time
                    make_a_turn(1,1.0)
                    time.sleep(0.2)
                    make_a_turn(1,1.0)
                    move(1,1.2)
                    #st()
                    #time.sleep(0.8)
                    #all_reset()
                    
                    
                elif (not io_data[6] and not io_data[7]) and (not io_data[4] or not io_data[5]):
                    # print("")
                    if io_data[4]:   # turn right ???
                        up.CDS_SetSpeed(1, -400)
                        up.CDS_SetSpeed(2, 400)
                        time.sleep(1.0)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        print("right null")
                        make_a_turn(1,1.0)
                        move(1, 1.3)
                        make_a_turn(1,1.0)
 
                        
                    elif io_data[5]:  # turn left ???
                        print("left null")
                        up.CDS_SetSpeed(1, -400)
                        up.CDS_SetSpeed(2, 400)
                        time.sleep(1.0)
                        up.CDS_SetSpeed(1, 0)
                        up.CDS_SetSpeed(2, 0)
                        make_a_turn(-1,1.0)
                        move(1, 1.3)
                        make_a_turn(-1,1.0)

                elif not io_data[4] and not io_data[5]:
                    print("left and right null")
                    make_a_turn(1,0.8)
#                     if table_flag == 1:
#                         print(count_time)
#                         count_time = count_time + 1
#                     if count_time >= 5:
#                         print("else -- 5")
#                         count_time = 0
#                         table_flag = 0
#                         move(-1,1)
#                         make_a_turn(1,0.5)
                    
                else:
                    print("else")
                    if table_flag == 1:
                        print(count_time)
                        count_time = count_time + 1
                    if count_time >= 5:
                        print("else -- 5")
                        count_time = 0
                        table_flag = 0
                        move(-1,1)
                        make_a_turn(1,0.5)
                    move(1,0.5)
                
                    
        except IndexError:
            print('Error:', IndexError)
    




