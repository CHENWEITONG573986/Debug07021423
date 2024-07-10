import uptech
import time

up=uptech.UpTech()

up.LCD_Open(2)
up.ADC_IO_Open()
up.ADC_Led_SetColor(0,0x000000)
up.ADC_Led_SetColor(1,0x000000)
up.CDS_Open()
for i in range(8):
    up.ADC_IO_SetIOMode(i,1)

up.CDS_SetMode(1,0)
up.MPU6500_Open()

up.LCD_PutString(30, 0, 'InnoStarTest')
up.LCD_Refresh()
up.LCD_SetFont(up.FONT_8X14)


flag=0

while True:
    
    attitude=up.MPU6500_GetAttitude()   
    str_attitude_pitch='Pitch:%.2f  ' % attitude[0]
    str_attitude_roll='Roll :%.2f  ' % attitude[1]
    str_attitude_yaw='Yaw  :%.2f  ' % attitude[2]

    up.LCD_PutString(0,30,str_attitude_pitch)
    up.LCD_PutString(0,44,str_attitude_roll)
    up.LCD_PutString(0,58,str_attitude_yaw)
    up.LCD_Refresh()
 
    if attitude[0] > 5:
        if flag ==0:
        
            up.CDS_SetAngle(1,300,300)
            up.ADC_Led_SetColor(0,0x0A0000)
            up.ADC_Led_SetColor(1,0x0A0000)
            for i in range(8):
                up.ADC_IO_SetIOLevel(i,1)
            flag =1
    elif attitude[0] <-5:
        if flag == 0:
            up.CDS_SetAngle(1,600,300)
            up.ADC_Led_SetColor(0,0x000A00)
            up.ADC_Led_SetColor(1,0x000A00)
            for i in range(8):
                up.ADC_IO_SetIOLevel(i,0)
            flag =1    
    else:

        flag = 0

        



    #time.sleep(0.5)

