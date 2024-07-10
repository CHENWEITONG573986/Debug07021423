from up_controller import UpController
import uptech
import time
import threading

servo_speed = 700
st_speed = 512
crush_speed = 768

up = uptech.UpTech()
up.CDS_Open()
up.LCD_Open(2)
open_flag = up.ADC_IO_Open()

controller = UpController()


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




if __name__ == '__main__':
    time.sleep(1)
    
    while True:
        
        if io_data[6] == 0:
            print("666")
            break
        elif io_data[7] == 0:
            print("777")
            break
        elif io_data[4] == 0:
            print("444")
            break
        elif io_data[5] == 0:
            print("555")
            break
        elif io_data[0] == 0:
            print("000")
            break
        elif io_data[1] == 0:
            print("111")
            break
        elif io_data[2] == 0:
            print("222")
            break
        elif io_data[3] == 0:
            print("333")
            break
        
        


    

