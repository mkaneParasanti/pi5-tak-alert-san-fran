### pi5-pir-tak-alert
Repo for workload to be used with UNITE in the demo kit. Uses python to generate a TAK pin centered in San Francisco.

### How to Setup
This mission workload utilizes a PIR sensor to detect motion.  If motion is detected then an LED light will turn on and an pin will appear on TAK. This mission workload uses Python3 with several python libraries to format the TAK curser on target message and TCP communication to the TAK server. This workload is specifically built for the GPIO of the Pi5, it will not work on older RPis.

The PIR out pin should be connected to GPIO 4 or PIN 7.

The LED power pin should be connected to GPIO 14 or pin 8.

### Install and Run Commands
# Script to install dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./demo-workload-main/requirements.txt --use-pep517
```
# Required shell command to start application
```venv/bin/python3 demo-workload-main/workload.py```

### References
PyTAK Example: https://pytak.readthedocs.io/en/latest/examples/
Pi PIR Sensor Example: https://projects.raspberrypi.org/en/projects/physical-computing/11
LED Light Example: https://roboticsbackend.com/raspberry-pi-control-led-python-3/

### How to Run
1. Ensure python3 and python3-pip are installed
    1. ``sudo apt install python3.10``
    2. ``sudo apt install python3-pip``
2. Run ``pip install -r requirements.txt``
3. Run ``python3 workload.py``