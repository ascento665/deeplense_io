import cv2
from time import sleep


cam = cv2.VideoCapture("/opt/awscam/out/ch2_out.mjpeg")
success, frame = cam.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
i = 0

while(True):
        # Capture frame-by-frame
        name = "pictures/movement.jpg"
        cv2.imwrite(name, frame)
        i +=1
        print "new file", i
        sleep(0.5)


print "finished streaming"
