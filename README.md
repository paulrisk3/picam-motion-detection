# picam-motion-detection
Motion detection and recording from IP camera using Python and OpenCV

## Getting Started
This script will probably run comfortably on a Pi 4 but would likely strain a Pi 3. I've got it running in Ubuntu 20.04 on a dual-core, hyper-threaded i3-2120 @ 3.30GHz with 12GB DDR3 RAM at about 30% CPU utilization and 2 GB of RAM.

Update - This does not actually run all that well on Raspberry Pi OS on Pi 4. I don't know why, at the moment. But it runs on Ubuntu. I'm going to leave it at that, for now. This code also runs just fine on Windows. The instructions to install OpenCV on Windows are a little different. I'll track that down.

### Prerequisites
sudo apt install python3-opencv

### Installation
git clone https://github.com/paulrisk3/picam-motion-detection.git

## Usage
python3 opencv_server.py `<IP Camera URL>`

### Need an IP Camera?
Check out my [pihomecam](https://github.com/paulrisk3/pihomecam)

## To do
* Auto-detect video framerate - defaults to 30fps
* Add running timestamp to recording
* Delete footage after defined number of days
* Add .conf file to register and name cameras
  * save footage by camera and date
* Add sources in README
* Configure alerts when motion is detected - likely MQTT
* Add instructions for Windows installation
* Fix videos recording too fast on Windows
* Optimize for Raspberry Pi OS on Pi 4
* Provide web server to view motion captures remotely
  * No. Just use Plex.

## Done
* Rebuild motion detection to not require status_list
  * If current motion_status == 1 and previous motion_status == 0, that's when we trigger motion.
