import cv2
from time import sleep
import numpy as np
import boto3


cam = cv2.VideoCapture("/opt/awscam/out/ch2_out.mjpeg")
firstFrame = None

resetter = 0
alert_counter = 0

sleep_counter = 0
sleep_state = False

s3 = boto3.client('s3')
bucket_name = 'temp-photo'

while True:
    if sleep_state == True:
        sleep_counter = sleep_counter + 1
        # print "sleeping"

    if sleep_counter > 10:
        sleep_state = False
        sleep_counter = 0

    # grab the current frame and initialize the occupied/unoccupied
    # text
    success, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # resize the frame, convert it to grayscale, and blur it
    # frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # reset reference image every ten iterations
    if resetter == 10:
        firstFrame = gray
        resetter = 0

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh_sum = np.sum(thresh) / float(10e6)

    if thresh_sum > 10 and sleep_state == False:
        # print thresh_sum
        sleep_counter = 0
        sleep_state = True
        # save picture
        name = "pictures/movement.jpg"
        cv2.imwrite(name, frame)
        sleep(0.1)
        # send picture to s3
        filename = name
        filename_dest = "uploads/movement.jpg"

        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        s3.upload_file(filename, bucket_name, filename_dest)
        print "motion detected and added to s3"

        # alert_counter = alert_counter + thresh_sum


    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
    	break

    resetter = resetter + 1

    # if alert_counter > 40:
    #     print "intrusion detected"
    #     alert_counter = 0
    #     sleep(2.0)

    sleep(0.1)

print "finished streaming"
