import cv2
import os

# save path 
SAVE_PATH = os.getcwd()

# video storage format
SAVE_FORMAT = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

# video storage frame
SAVE_FPS = 14

# video transmission format
FRAME_QUALITY = 15

# default resolution
DEFAULT_RESOLUTION = (640,480)

# default address of raspberry
DEFAULT_ADDRESS = ("192.168.1.101", 6666)

# picture size
CONST_BUFFER_SIZE = DEFAULT_RESOLUTION[0] * DEFAULT_RESOLUTION[1]

# const time to save picture
CONST_TIME = 4