import cv2
import datetime
import sys
import os
import time
import configparser
from multiprocessing import Process

def detect_motion(config, key):
    # Boolean to assist with printing debug statements
    camera_connected = False

    while True:
        try:
            baseline_image=None
            # This status thing just gets bigger and bigger. What's the purpose of keeping track of it outside of the immediate cycle?
            status_list=[None, None]
            video=cv2.VideoCapture(config[key]['url'])
            record_length = 10
            size = (config[key]['x_resolution'], config[key]['y_resolution'])
            framerate = config[key]['fps']
            baseline_counter=0

            while True:
                check, frame = video.read()
                # If camera was not previously connected, print connected message
                if camera_connected == False:
                    camera_connected = True
                    print("Connected to " + key)
                motion_status=0
                gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

                # Reset the baseline_counter every 300 frames
                if baseline_counter == 300:
                    baseline_counter=0
                baseline_counter = baseline_counter+1

                # Reset baseline_image to the current gray_frame after every 300 frames
                if baseline_counter==1:
                    baseline_image=gray_frame
                    continue

                delta=cv2.absdiff(baseline_image,gray_frame)
                threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
                (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    if cv2.contourArea(contour) < 10000:
                        continue
                    motion_status=1
                    (x, y, w, h)=cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
                status_list[0] = status_list[1]
                status_list[1] = motion_status

                # If motion is detected, record for record_length seconds
                if status_list[1]==1 and status_list[0]==0:
                    now = datetime.datetime.now()
                    print("Motion detected at " + str(now))
                    clip_directory = 'clips/' + now.strftime('%Y/%m-%B/%d-%A/') 
                    if not os.path.exists(clip_directory):
                        os.makedirs(clip_directory)
                    video_clip = cv2.VideoWriter(clip_directory + now.strftime("%Y-%m-%d_%H-%M-%S") + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), framerate, size)
                    time_end = record_length + time.time()
                    while time.time() < time_end:
                        # print(time.time())
                        check, frame = video.read()
                        video_clip.write(frame)
                    video_clip.release()

                key=cv2.waitKey(1)

                if key==ord('q'):
                    if status==1:
                        times.append(datetime.datetime.now())
                    break

            video.release()
        except:
            video.release()
            # If an error is hit, mark the camera_connected flag as False.
            camera_connected = False
            print("Retrying connection to ", key, " in 10 seconds...")
            time.sleep(10)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('picam-motion-detection.conf')
    for key in config.sections():
      p = Process(target=detect_motion(config, key))
      #jobs.append(p)
      p.start()
