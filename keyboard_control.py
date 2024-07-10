import uptech
import time
import cv2
import threading
import sys, select, termios, tty

def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.speed = 512
        self.direction = 0

        self.done = False
        self.up = uptech.UpTech()
        '''
        init uptech
        '''
        self.up.LCD_Open(2)
        self.up.ADC_IO_Open()
        self.up.CDS_Open()
        self.up.MPU6500_Open()

        self.up.LCD_PutString(30, 0, 'InnoStar')
        self.up.LCD_Refresh()
        self.up.LCD_SetFont(self.up.FONT_8X14)

        self.up.CDS_SetMode(1,1)
        self.up.CDS_SetMode(2,1)
        self.up.CDS_SetMode(3,1)
        self.up.CDS_SetMode(4,1)
        self.up.CDS_SetMode(5,0)
        self.up.CDS_SetMode(6,0)

        self.condition = threading.Condition()
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None
        self.start()
    
    def update(self, direction, speed):
        self.condition.acquire()
        self.speed = speed
        self.direction = direction
        self.condition.notify()
        self.condition.release()
    
    def stop(self):
        self.done = True
        self.update(0, 0)
        self.join()
    
    def run(self):
        while not self.done:
            self.condition.acquire()
            self.condition.wait(self.timeout)
            if (self.direction == 0):
                self.up.CDS_SetSpeed(1, self.speed)
                self.up.CDS_SetSpeed(2, -self.speed)
                self.up.CDS_SetSpeed(3, self.speed)
                self.up.CDS_SetSpeed(4, -self.speed)
            elif (self.direction == 1):
                self.up.CDS_SetSpeed(1, -self.speed)
                self.up.CDS_SetSpeed(2, self.speed)
                self.up.CDS_SetSpeed(3, -self.speed)
                self.up.CDS_SetSpeed(4, self.speed) 
            elif (self.direction == 2):
                self.up.CDS_SetSpeed(1, -self.speed)
                self.up.CDS_SetSpeed(2, -self.speed)
                self.up.CDS_SetSpeed(3, self.speed)
                self.up.CDS_SetSpeed(4, self.speed) 
            elif (self.direction == 3):
                self.up.CDS_SetSpeed(1, self.speed)
                self.up.CDS_SetSpeed(2, self.speed)
                self.up.CDS_SetSpeed(3, -self.speed)
                self.up.CDS_SetSpeed(4, -self.speed)                           
            self.condition.release()

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin) 
    pub_thread = PublishThread(0.0)
    direction = 0
    speed = 0
    try:
        pub_thread.update(direction, speed)
        while(1):
            key = getKey(0.0)
            if (key == 'w'):
                direction = 0
                speed = 512
            elif (key == 's'):
                direction = 1
                speed = 512
            elif (key == 'a'):
                direction = 2
                speed = 512
            elif (key == 'd'):
                direction = 3
                speed = 512
            elif (key == 'x'):
                direction = 0
                speed = 0
            else:
                if (key == ''):
                    continue               
                if (key == 'q'):
                    break
            pub_thread.update(direction, speed)
    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

