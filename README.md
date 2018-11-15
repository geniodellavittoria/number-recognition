Tutorial: https://www.hackster.io/dhq/ai-digit-recognition-with-picamera-2c017f 

1. install Python (Version 3.6.7) check with python --version
2. install pip https://www.makeuseof.com/tag/install-pip-for-python/
3. pip install numpy
4. pip install scikit-image
5. pip install scipy
6. pip install keras
7. pip install opencv-python
8. pip install imutils
9. pip install tensorflow (https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip)

--------------
MacOS:

1. install python3 (Version 3.6.7) check with python --version
2. install pip3 https://www.makeuseof.com/tag/install-pip-for-python/
3. pip3 install numpy
4. pip3 install scikit-image
5. pip3 install scipy
6. pip3 install keras
7. pip3 install opencv-python
8. pip3 install imutils
9. pip3 install tensorflow (https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip)
10. 
--------------
https://hackernoon.com/raspberry-pi-headless-install-462ccabd75d0

Raspbian Stretch LITE: https://www.raspberrypi.org/downloads/raspbian/

SSH: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

# Example static IP configuration:
interface eth0
static ip_address=192.168.1.23/24
static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8 fd51:42f8:caae:d92e::1

Take Photo: raspistill -o testbild.jpg