# Raspberry Pi ISS Tracker

Get alerts when the ISS space station passes nearby using Raspberry Pi and Sense Hat

## Installation:

1. Open a Terminal on your Raspberry Pi
2. Add the following line to the end of /boot/config.txt as sudo
```hdmi_force_hotplug=1```
3. Synchronise the change
```sync```
4. Reboot
```sudo reboot```
5. Open a terminal
6. Install Haversign
```pip3 install haversine```
7. Clone the repo
```git clone https://github.com/LetsOKdo/raspberry-pi-iss-tracker.git```
8. Change to the project directory
```cd raspberry-pi-iss-tracker```
9. Run the python code
```python3 ./sensehat-iss.py```
