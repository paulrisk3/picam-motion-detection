import cv2
import datetime
import sys
import os
import time
import configparser
from multiprocessing import Process

def detect_motion(config, camera_name):
    try:
        camera_url = config[camera_name]['url']
        record_length = int(config[camera_name]['record_time'])
        framerate = int(config[camera_name]['fps'])
        reconnect_time = int(config[camera_name]['reconnect_time'])
        baseline_counter=0
        baseline_image=None
        status_list=[None, None]
        camera_connected = False

    except KeyError as e:
        print(e,"appears to be misconfigured for",camera_name,"in",config_file_location)
        print("Please check",config_file_location,"and fix any errors.")
        sys.exit()

    while True:
        try:
            video=cv2.VideoCapture(camera_url)
            if not video.isOpened():
              raise ConnectionError
            check, frame = video.read()
            # If camera was not previously connected, print connected message
            if camera_connected == False:
                camera_connected = True
                print("Connected to ", camera_name)
            size=(int(video.get(3)), int(video.get(4)))
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
                clip_directory = 'clips/' + now.strftime('%Y/%m-%B/%d-%A/') + camera_name + '/'
                if not os.path.exists(clip_directory):
                    os.makedirs(clip_directory)
                try:
                  video_clip = cv2.VideoWriter(clip_directory + now.strftime("%Y-%m-%d_%H-%M-%S") + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), framerate, size)
                  time_end = record_length + time.time()
                  while time.time() < time_end:
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

        except ConnectionError:
            video.release()
            camera_connected = False
            print("Retrying connection to",camera_name,"in",str(reconnect_time),"seconds...")
            time.sleep(reconnect_time)
      
    video.release()

if __name__ == '__main__':
  try:
    config_file_location = 'picam-motion-detection.conf'
    if not os.path.exists(config_file_location):
        raise FileNotFoundError
    config = configparser.ConfigParser()
    config.read(config_file_location)
    jobs=[]
    for camera_name in config.sections():
      p = Process(target=detect_motion, args=[config, camera_name])
      jobs.append(p)
      p.start()
    for p in jobs:
      p.join()
  
  except FileNotFoundError:
    print("opencv-server.py could not find picam-motion-detection.conf")
    print("Make sure that",config_file_location,"exists in the same directory as this script and is configured correctly.")

  except Exception as e:
    print(e)

