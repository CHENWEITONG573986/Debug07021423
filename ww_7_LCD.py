#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
import threading

import socket
import fcntl
import struct
import os

#fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))
# def get_ip_address():
#     s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     s.connect(("1.1.1.1",80))
#     ipaddr=s.getsockname()[0]
#     s.close()
#     return ipaddr
    #return socket.inet_ntoa(0xff553644)

def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
                s.fileno(), 
                0x8915, # SIOCGIFADDR 
                struct.pack('256s', ifname[:15]) 
                )[20:24])
up=uptech.UpTech()

up.LCD_Open(2)
hostname = "Host:" + socket.gethostname() 


#up.CDS_SetMode(1,up.CDS_MODE_SERVO)
#up.CDS_SetSpeed(1,512)

fore_color = up.COLOR_GREEN
back_color = up.COLOR_BLACK

up.LCD_SetForeColor(fore_color)
up.LCD_SetBackColor(back_color)
up.LCD_FillScreen(back_color)
up.LCD_SetFont(up.FONT_8X14)
time.sleep(2.0)
count = 0
sign = 0
sign2 = 0

date = time.strftime("%Y-%m-%d")
tt = time.strftime('%H:%M:%S')


    #up.LCD_FillScreen(back_color)
up.LCD_SetForeColor(up.COLOR_BRED)

up.LCD_PutString(0, 0,hostname)
up.LCD_PutString(0, 16, get_ip_address('wlan0'))


up.LCD_SetForeColor(fore_color)

up.LCD_PutString(0,32,"Open Time:")
up.LCD_PutString(0, 48, date)
up.LCD_PutString(0, 64, tt)


up.LCD_SetForeColor(up.COLOR_LIGHTGREEN)
    
up.LCD_Refresh()
time.sleep(0.05)



up.stop()






