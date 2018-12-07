Tutorial: https://www.hackster.io/dhq/ai-digit-recognition-with-picamera-2c017f 

1. install Python (Version 3.6.7) check with python --version
2. install pip https://www.makeuseof.com/tag/install-pip-for-python/
3. `pip install numpy`
4. `pip install scikit-image`
5. `pip install scipy`
6. `pip install keras`
7. `pip install opencv-python`
8. `pip install imutils`
9. `pip install tensorflow` (https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip)

--------------
MacOS:

1. install python3 (Version 3.6.7) check with python --version
2. install pip3 https://www.makeuseof.com/tag/install-pip-for-python/
3. `pip3 install numpy`
4. `pip3 install scikit-image`
5. `pip3 install scipy` 
6. `pip3 install keras`
7. `pip3 install opencv-python`
8. `pip3 install imutils`
9. `pip3 install tensorflow` (https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip)

--------------
# Raspberry Pi
Allgemeine Installationsanleitung:
* https://hackernoon.com/raspberry-pi-headless-install-462ccabd75d0

## Betriebssystem
Raspbian Stretch LITE:
* https://www.raspberrypi.org/downloads/raspbian/

## Verbindung
SSH:
* https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

## Installation
https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
1. `sudo apt-get install python3-pip`
2. `sudo apt-get install python3-picamera`
3. `pip3 install numpy` (Version 1.15.4)
4. `pip3 install scikit-image` (scikit-image-0.14.1)
5. `pip3 install scipy` (scipy-1.1.0)
6. `pip3 install keras` (keras-2.2.4 keras-applications-1.0.6 keras-preprocessing-1.0.5)
7. `pip3 install opencv-python` (opencv-python-3.4.3.18)
8. `pip3 install imutils` (imutils-0.5.1)
9. ~~`pip3 install tensorflow` (tensorflow-1.11.0) (Troubleshooting: https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip)~~
10. `wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.9.0/tensorflow-1.9.0-cp35-none-linux_armv7l.whl -P /tmp/`
11. `pip install  /tmp/tensorflow-1.9.0-cp35-none-linux_armv7l.whl`

## Konfigurationen

Static IP configuration (`sudo nano /ect/dhcpcd.conf`):
```
interface eth0
static ip_address=192.168.1.23/24
static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8 fd51:42f8:caae:d92e::1
```

## Befehle

Take Photo: `raspistill -o testbild.jpg`
Take Video: `raspivid -o - -t 0 -n -w 600 -h 400 -fps 12 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264`
http://www.raspberry-projects.com/pi/pi-hardware/raspberry-pi-camera/streaming-video-using-vlc-player

# Troubleshooting Raspberry Pi
"Import Error: libf77blas.so.3: cannot open shared object file: No such file or directory" -> `sudo apt-get install libatlas-base-dev`
"ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory" -> `sudo apt-get install libopenjp2-7`
"ImportError: libtiff.so.5: cannot open shared object file: No such file or directory" -> `sudo apt install libtiff5`
"ImportError: libwebp.so.6: cannot open shared object file: No such file or directory" -> `sudo apt install libwebp6`
"ImportError: libjasper.so.1: cannot open shared object file: No such file or directory" -> `sudo apt install libjasper1`
"ImportError: libImath-2_2.so.12: cannot open shared object file: No such file or directory" -> `sudo apt install libilmbase-dev`