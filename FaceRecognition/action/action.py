from action import uptech
import time

class Controller:
    def __init__(self) -> None:
        self.up= uptech.UpTech()
        self.SPEED = 250


    def setMode(self):
        self.up.CDS_Open()
        self.up.CDS_SetMode(5, 0)
        self.up.CDS_SetMode(6, 0)
        self.up.CDS_SetMode(7, 0)
        self.up.CDS_SetMode(8, 0)
        self.up.CDS_SetMode(9, 0)
        self.up.CDS_SetMode(10, 0)
        self.up.CDS_SetMode(11, 0)
        self.up.CDS_SetMode(12, 0)
        self.up.CDS_SetMode(13, 0)
        self.up.CDS_SetMode(14, 0)
        self.up.MPU6500_Open()  
    
    def resetAngle(self):
        self.up.CDS_SetAngle(5, 508, 300)
        self.up.CDS_SetAngle(6, 305, 300) 
        self.up.CDS_SetAngle(7, 964, 300)
        self.up.CDS_SetAngle(8, 236, 300)
        self.up.CDS_SetAngle(9, 501, 300)
        self.up.CDS_SetAngle(10, 512, 300)
        self.up.CDS_SetAngle(11, 661, 300)
        self.up.CDS_SetAngle(12, 91, 300)
        self.up.CDS_SetAngle(13, 512, 300)
        self.up.CDS_SetAngle(14, 512, 300)
        time.sleep(1)


    def swing_arm(self):
        self.up.CDS_SetAngle(5, 613, 300)
        self.up.CDS_SetAngle(10, 579, 300)
        time.sleep(1)
        self.up.CDS_SetAngle(5, 403, 300)
        self.up.CDS_SetAngle(10, 450, 300)
        time.sleep(1)
        self.up.CDS_SetAngle(5, 613, 300)
        self.up.CDS_SetAngle(10, 579, 300)
        time.sleep(1)
        self.up.CDS_SetAngle(5, 403, 300)
        self.up.CDS_SetAngle(10, 450, 300)
        time.sleep(1)
        self.up.CDS_SetAngle(5, 508, 300)
        self.up.CDS_SetAngle(10, 512, 300)
        time.sleep(1)


    def stretch_arm(self):
        self.up.CDS_SetAngle(5,  810,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(6,  287,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(7,  396,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(9,  400,  300)
        time.sleep(1)



    def bend_arm(self):
        self.up.CDS_SetAngle(9,  501,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(7,  964,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(6,  305,  300)
        time.sleep(1)
        self.up.CDS_SetAngle(5,  508,  300)
        time.sleep(1)


if __name__ == '__main__':
    ctrl = Controller()
    ctrl.setMode()
    ctrl.resetAngle()
    ctrl.swing_arm()
    ctrl.stretch_arm()
    ctrl.bend_arm()

