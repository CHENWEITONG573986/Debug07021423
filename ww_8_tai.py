from up_controller import UpController
import uptech
import cv2


up = uptech.UpTech()
up.CDS_Open()
up.LCD_Open(2)
open_flag = up.ADC_IO_Open()
controller = UpController()
io_data = []

flag = False	

def get_io_value():
    global flag
    while True:
        adc_data = up.ADC_Get_All_Channle()
        #taixia:   [0]<=1500,[1]<=900
        flag = False if adc_data[0] < 2200 or adc_data[1] < 1200 else True
        io_all_input = up.ADC_IO_GetAllInputLevel()
        # print("io_vaule = {}".format(io_all_input))
        io_array = '{:08b}'.format(io_all_input)
        io_data.clear()
        for index, value in enumerate(io_array):
            io_value = (int)(value)
            io_data.insert(0, io_value)
        if flag:
            print("1")
        else:
            print("2")
        print('---', flag, adc_data[0], adc_data[1])

get_io_value()
