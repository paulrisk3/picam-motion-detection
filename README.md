# picam-motion-detection
Motion detection and recording from IP camera using Python and OpenCV

## Getting Started
I've got this running in Ubuntu 20.04 on a dual-core, hyper-threaded i3-2120 @ 3.30GHz with 12GB DDR3 RAM at about 30% CPU utilization and 200 MB of RAM. It also runs on Windows. All you need are Python 3, the OpenCV Python library, and the opencv-server.py script provided in this repository.

A note for the Raspberry Pi users out there - OpenCV for Python doesn't run well on Pi. If you're a mage, you can install it properly and then maybe get this script running. I don't have emotional time for that.

### Prerequisites

#### Install Python 3
* Linux: You've probably already got it. `python --version`
* Windows: [Python Releases for Windows](https://www.python.org/downloads/windows/)

#### Install OpenCV for Python
* Linux: sudo apt install python3-opencv
* Windows: pip install opencv-python

### Installation
git clone https://github.com/paulrisk3/picam-motion-detection.git

## Usage
The motion detection script reads from picam-motion-detection.conf to find the names and URLs for your IP cameras. A sample file is provided in the repo. You should edit that file directly, replacing the names in [brackets] with your desired camera names, and the url variable with the URL for the corresponding IP camera. If you're using my [pihomecam](https://github.com/paulrisk3/pihomecam), then you should leave the fps at 30.  

python3 opencv_server.py

### Need an IP Camera?
Check out my [pihomecam](https://github.com/paulrisk3/pihomecam)

## Acknowledgements
Props to Arindom Bhattacharjee at [towards data science](https://towardsdatascience.com/build-a-motion-triggered-alarm-in-5-minutes-342fbe3d5396) for teaching me how to use OpenCV for Python. Much of my code is taken from their blog post.

## To do
* Auto-detect video framerate - defaults to 30fps
* Add running timestamp to recording
* Delete footage after defined number of days
* Configure alerts when motion is detected - likely MQTT
* Fix videos recording too fast on Windows
  * Working on it.
* Optimize for Raspberry Pi OS on Pi 4
  * That's not going to happen any time soon. The OpenCV library does **not** like Pi.
* Provide web server to view motion captures remotely
  * No. Just use Plex.

## Done
* Rebuild motion detection to not require status_list
  * If current motion_status == 1 and previous motion_status == 0, that's when we trigger motion.
* Add .conf file to register and name cameras
  * Save footage by camera and date
* Add sources in README
* Add instructions for Windows installation
