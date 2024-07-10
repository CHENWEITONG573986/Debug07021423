from up_controller import UpController
import time
import uptech
flag = 40
print(flag)
class go_up_platform_AND_manyou:
    def __init__(self):
       self.controller = UpController()
    def stagedetect(self):
            data = self.controller.adc_data
            #print("stagedetect")
            if len(data) ==0:
                return -1
            #print("data",data)
            
            print('data0:', data[0])
            
            print('data1:', data[1])
if __name__ == '__main__':
    A = go_up_platform_AND_manyou()
    while True:
        A.stagedetect()
        time.sleep(1.0)
