import os

path = os.getcwd()
os.chdir(os.path.pardir)
# save path 
SAVE_PATH = os.getcwd()
os.chdir(path)

# video storage frame
SAVE_FPS = 16

# video transmission format
FRAME_QUALITY = 15

# default resolution
DEFAULT_RESOLUTION = (640,480)

# default address of raspberry
# 192.168.1.103
DEFAULT_ADDRESS = ("192.168.43.60", 7999)

# picture size
CONST_BUFFER_SIZE = DEFAULT_RESOLUTION[0] * DEFAULT_RESOLUTION[1]

# const time to save picture
CONST_TIME = 4
