#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
count=0
sign=0

if __name__ == '__main__':
    up=uptech.UpTech()
    up.CDS_Open()
    up.CDS_SetSpeed(1, 400)
    up.CDS_SetSpeed(2, -400)
    time.sleep(1.0)
    up.CDS_SetSpeed(1, -500)
    up.CDS_SetSpeed(2, -500)
    time.sleep(1.5)
#     up.CDS_SetSpeed(1, 400)
#     up.CDS_SetSpeed(2, -400)
#     time.sleep(1.0)
#     up.CDS_SetSpeed(1, -500)
#     up.CDS_SetSpeed(2, -500)
#     time.sleep(0.5)
    up.CDS_SetSpeed(1, 0)
    up.CDS_SetSpeed(2, 0)


    





