import cv2
import os

# save path 
SAVE_PATH = os.getcwd() + "/Video/"

# video storage format
SAVE_FORMAT = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

# video storage frame
SAVE_FPS = 11

# video transmission format
FRAME_QUALITY = 12

# default resolution
DEFAULT_RESOLUTION = (640,480)

# default address of raspberry
DEFAULT_ADDRESS = ("192.168.1.101", 7999)

# picture size
CONST_BUFFER_SIZE = DEFAULT_RESOLUTION[0] * DEFAULT_RESOLUTION[1]
