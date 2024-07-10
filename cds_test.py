#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
count=0
sign=0

if __name__ == '__main__':
    up=uptech.UpTech()
    up.CDS_Open()
    while True:
        if count == 0:
            up.CDS_SetSpeed(1,220)
            up.CDS_SetSpeed(2,300)
            count = 1
        else:
            count = 0
            up.CDS_SetSpeed(1,-220)
            up.CDS_SetSpeed(2,300)
        time.sleep(3)


    




