import cv2
import datetime
import sys
import os
import time
import configparser
from multiprocessing import Process

def detect_motion(config, camera_name):
    camera_connected = False

    while True:
        try:
            baseline_image=None
            status_list=[None, None]
            video=cv2.VideoCapture(config[camera_name]['url'])
            record_length = 10
            size=(int(video.get(3)), int(video.get(4)))
            framerate = config[camera_name]['fps']
            baseline_counter=0

            while True:
                check, frame = video.read()
                # If camera was not previously connected, print connected message
                if camera_connected == False:
                    camera_connected = True
                    print("Connected to " + camera_name)
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
                    print("Motion detected from " + camera_name + " at " + str(now))
                    clip_directory = 'clips/' + now.strftime('%Y/%m-%B/%d-%A/') 
                    if not os.path.exists(clip_directory):
                        os.makedirs(clip_directory)
                    print("Preparing video clip.")
                    try:
                      #The crash happens when motion is detected and it hits this line.
                      print("Directory: ", clip_directory)
                      print("Framerate: ", framerate)
                      print("Size: ", size)
                      video_clip = cv2.VideoWriter(clip_directory + now.strftime("%Y-%m-%d_%H-%M-%S") + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), framerate, size)
                      print("Calculating record length.")
                      time_end = record_length + time.time()
                      print("Begin writing.")
                      while time.time() < time_end:
                        # print(time.time())
                        check, frame = video.read()
                        video_clip.write(frame)
                      video_clip.release()
                    except Exception as e:
                      print(e)

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
            print("Retrying connection to ", camera_name, " in 10 seconds...")
            time.sleep(10)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('picam-motion-detection.conf')
    jobs=[]
    for camera_name in config.sections():
      p = Process(target=detect_motion, args=[config, camera_name])
      jobs.append(p)
      p.start()
    #for p in jobs:
      #p.join()
