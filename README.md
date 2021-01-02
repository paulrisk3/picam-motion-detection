# picam-motion-detection

## Getting Started
This script will probably run comfortably on a Pi 4 but would likely strain a Pi 3. I've got it running in Ubuntu 20.04 on a dual-core, hyper-threaded i3-2120 @ 3.30GHz with 12GB DDR3 RAM at about 30% CPU utilization and 2 GB of RAM.

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
* Rebuild motion detection to not require status_list - currently grows larger forever
  * If current motion_status == 1 and previous motion_status == 0, that's when we trigger motion.
  * We don't need to keep track of the status *forever*, but we do need the previous and current status. 
  * That will be easy to replace.
* Delete footage after defined number of days
* Add .conf file to register and name cameras
  * save footage by camera and date
* Add sources in README
* Configure alerts when motion is detected - likely MQTT
