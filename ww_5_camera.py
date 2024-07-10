import cv2
import apriltag

cap = cv2.VideoCapture(2)
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))

# ...
w = 640#640
h = 480#480
#     weight =320#320  #520
weight = 320
cap.set(3,w)
cap.set(4,h)

id = 0

cup_w = (int)((w - weight) / 2)
cup_h = (int)((h - weight) / 2) + 50   #   bian jie she zhi
    
while True:
    try:
        ret, frame = cap.read()
        frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
        id = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        tags = at_detector.detect(gray)
        
        tag_id = tags[0].tag_id if len(tags) else -1
        print(tag_id)
        
        cv2.imshow('video', frame)
        c = cv2.waitKey(1) & 0xff
        if c == 27:
            cap.release()
            break
    except Exception as e:
        print("Exception:", e)
        # 在此处添加重新启动线程的代码
        cap.release()
        cap = cv2.VideoCapture(id)
        id = id +1
        at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        continue
        
cap.release()
cv2.destroyAllWindows()