import cv2
import datetime

baseline_image=None
# This status thing just gets bigger and bigger. What's the purpose of keeping track of it outside of the immediate cycle?
status_list=[None, None]
# Replace 0 with URL of network camera
video=cv2.VideoCapture("http://192.168.1.126:8000/stream.mjpg")
# video=cv2.VideoCapture(0)
baseline_counter=0

while True:
    check, frame = video.read()
    status=0
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if baseline_counter == 300:
        baseline_counter=0
    baseline_counter = baseline_counter+1

    if baseline_counter==1:
        baseline_image=gray_frame
        continue

    delta=cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
    status_list.append(status)

    if status_list[-1]==1 and status_list[-2]==0:
        print("Motion detected at " + str(datetime.datetime.now()))

    # cv2.imshow("gray_frame Frame",gray_frame)
    # cv2.imshow("Delta Frame",delta)
    # cv2.imshow("Threshold Frame",threshold)
    # cv2.imshow("Color Frame",frame)

    # key=cv2.waitKey(1)

    # if key==ord('q'):
    #     if status==1:
    #         times.append(datetime.datetime.now())
    #     break

video.release()
cv2.destroyAllWindows
