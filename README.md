# Using Environment:
  1.python3.6 ++
  2.opencv, socket, struct, datetime
  3.pytorch1.0.1 ++
  4.linux(linux + linux or linux + respberry) //the respberry is client to collect the video,and running server.py on PC.
  5.object detection model is yolov3, from:https://github.com/ultralytics/yolov3  not exactly the same as the original template.
  6.Peripheral：USB camera (must support the UVC protocol), your Laptop's camera is also supposed.

# Introduction
  This program use python-opencv to get video and transmit the video from WiFi .It can work on any machine that can use python-opencv.
  This project use of USB camera to capture video, and the video is transmitted to another computer through the Route for storage and display, with high real-time performance, it used yolov3 model to detect the object.

# Start :
  There are three things to note when starting this program ：
    1.Used the python3 to start server.py(client.py) on Linux
    2.If you want this project work in different floder(machine), please put camer.py,client.py(server.py) and config.py in the same floder
    3.Change the Ip
  
# Start Using This:
    1. python3 server.py
      start server to receive video frame
    2. python3 client.py
      start client to send video frame
    3. you can stop it working when you selected the cv2.imshow's windows then clicking the 'q', it will shut down Client working, Server will running but will not receive any data untill the next socket. 

# Other Description：
  Most errors in this project run will write in the Error_log, this log file will automatically generate.
  All output information will write in the Running_log.~
  It can work on Raspberry or other linux base on the python.
  
