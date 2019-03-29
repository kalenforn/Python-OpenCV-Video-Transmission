import socket  
# import threading  
import struct  
import os               
import time  
import sys
import re
import traceback

import numpy as np

from config import (DEFAULT_ADDRESS, SAVE_PATH, FRAME_QUALITY, CONST_BUFFER_SIZE, DEFAULT_RESOLUTION, SAVE_FPS, SAVE_FORMAT)
from camer import VideoFrame

class Client:
    
    def __init__(self, address=DEFAULT_ADDRESS, savePath=SAVE_PATH, frameQuality=FRAME_QUALITY, 
                    resolution=DEFAULT_RESOLUTION, saveFrame=SAVE_FPS, saveFormat=SAVE_FORMAT):

        # initial dynamic parameter of saving used

        self.__address = address
        self.__savePath = savePath + "/Video/"
        # 传输图像质量，0～100，值越高图片质量越高，但是在低速网络中值越大传输失败率也随之增大
        self.__frameQuality = frameQuality
        # self.__transSize = transSize
        self._video = VideoFrame(resolution, saveFrame, saveFormat)
        self._FPS = 0

        # 确保savePath存在
        try:
            os.mkdir(self.__savePath)
            info = "Made Dir:{}".format(self.__savePath)
            self._write_ordinary_logs(info)
        except:
            pass

        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        self._save_floder = self.__savePath + str(tm_year) + "_" + str(tm_mon) + "_" + str(tm_mday) + "/"
        try:
            os.mkdir(self._save_floder)
            info = "Made Dir:{}".format(self._save_floder)
            self._write_ordinary_logs(info)
        except:
            pass

        self._file_name = self._save_floder + "video_"  + str(tm_hour) + "_" + str(tm_min) + "_" + str(tm_sec) + ".mp4"
        try:
            os.mknod(self._file_name)
            info = "Touch File:{}".format(self._file_name)
            self._write_ordinary_logs(info)
        except:
            pass

        self._video.setVideoWriter(self._file_name)
        self._start_time = { "year": 2019, "month": 3, "day": 13, "hour":0, "min":0, "sec":0}
        self._count_frame = 0
    
    # 写出错日志
    def _write_error_logs(self, e):

        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        with open("Error_log_client", 'a+') as f:
            f.writelines("\n*********************************************************************\n")
            f.write("Error:time:{0:4d}/{1:2d}/{2:2d},{3:2d}:{4:2d}:{5:2d}\\\\\n:{6}".format(tm_year, 
                        tm_mon, tm_mday, tm_hour, tm_min, tm_sec, traceback.format_exc()))
            f.writelines("*********************************************************************\n")
    
    # 写普通运行结果日志
    def _write_ordinary_logs(self, info, head=True):
        
        assert isinstance(info, str)
        assert isinstance(head, bool)

        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        with open('Run_log_client', 'a+') as f:
            if head :
                f.writelines("\n*********************************************************************\n")
            f.write("INFO:time:{0:4d}/{1:2d}/{2:2d},{3:2d}:{4:2d}:{5:2d}\\\\{6}".format(tm_year, 
                        tm_mon, tm_mday, tm_hour, tm_min, tm_sec, info + "\n"))

    # 创建socket连接
    def _connectting(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.connect(self.__address)
            info = "Socket connected, address: {}".format(self.__address[0])
            self._write_ordinary_logs(info)
            # print(info)
        except Exception as e: #ConnectionRefusedError
            self._write_error_logs(e)
            # print(e)

    # 判断是否需要重新创建writer，并且release掉writer保存视频
    def _isCreateNewWriter(self):
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        # 上面的flag是以一小时作为存储的判断条件，下面的flag是以一分钟作为存储判断条件
        flag = ((self._start_time["sec"] == tm_sec and self._start_time["min"] == tm_min) and 
                    (self._start_time["hour"] + 1 == tm_hour if self._start_time["hour"] != 23 else tm_hour == 0))
        """flag = (self._start_time["sec"] == tm_sec and 
            (self._start_time["min"] + 1 == tm_min if self._start_time["min"] != 59 else tm_min == 0))"""

        
        if flag:
            self._video.saveRelease()
            info = "File save at: {0}\nFPS: {1}".format(self._file_name, self._video.getFrame())
            self._write_ordinary_logs(info, False)
            # print("INFO:time: {0:4d}/{1:2d}/{2:2d},{3:2d}:{4:2d}:{5:2d}, File save at :{6}\nNumber of frame is {7:04d}".format(tm_year, 
             #                       tm_mon, tm_mday, tm_hour, tm_min, tm_sec, self._file_name, self._count_frame))
            
            if tm_mday != self._start_time["day"]:
                self._save_floder = self.__savePath + str(tm_year) + "_" + str(tm_mon) + "_" + str(tm_mday) + "/"
                try:
                    os.mkdir(self._save_floder)
                except:
                    pass

            self._file_name = self._save_floder + "video_" + str(tm_hour) + "_" + str(tm_min) + "_" + str(tm_sec) + ".mp4"
            try:
                os.mknod(self._file_name)
            except:
                pass

            self._video.setVideoWriter(self._file_name)
            self._start_time.update({"year": tm_year, "month": tm_mon, "day": tm_mday, 
                "hour":tm_hour, "min":tm_min, "sec":tm_sec})
            self._video.clearFrame()


    # 保存视频
    def _save_video(self, buffer):
        
        self._isCreateNewWriter()
        self._video.addFrame()
        self._video.writeVideo(buffer)

    # 启动所有任务
    def run(self):

        resolution = self._video.getResolution()
        # print(type(resolution[0]), type(resolution[1]))
        send_data = struct.pack('iii',self.__frameQuality, 
                                    resolution[0], resolution[1])
        self._connectting()
        # print("Send data,", send_data)
        self._socket.send(send_data)
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        self._start_time.update({"year": tm_year, "month": tm_mon, "day": tm_mday, 
                "hour":tm_hour, "min":tm_min, "sec":tm_sec})
        self._start_clock = time.time()

        """bufSize = self._socket.recv(4)
        print(bufSize)
        bufSize = struct.unpack('i', bufSize)[0]
        print(bufSize)
        """

        while True:
            # 传过来的内容包含两部分，一部分是总的图片大小，另一部分就是图片数据，前4字节是图片大小
            bufSize = self._socket.recv(4)
            bufSize = struct.unpack('i', bufSize)[0]
            buffer = b''
            # print(bufSize)
            try:
                while bufSize: #循环采集一张图片
                    data = self._socket.recv(bufSize)
                    bufSize -= len(data)
                    buffer += data
                # 图片通过socket传送后的一种编解码的方式
                buffer = np.fromstring(buffer, dtype=np.uint8)
                buffer = self._video.imdecode(buffer)
                self._save_video(buffer)
                self._video.showVidoe(buffer)
            except Exception as e:
                self._write_error_logs(e)
                self._isCreateNewWriter()
             #   print(e)
              #  break
            finally:
                if self._video.waitetime(10) == 27:
                    self._socket.close()
    
    # 公共接口，是为了防止程序出现意外的bug其内部信息丢失
    def close(self):
        if self._socket != None :
            self._socket.close()
        self._video.destroyAllWindows()

def main():
    while True:

        try:
            client = Client()
            #while True:
            client.run()
        except Exception as e:
            # 这个地方的日志处理有点问题，需要修改，异常抛出以后文件是更新了，但是内存里的FPS没有更新和写入log文件
            client._write_error_logs(e)
        finally:
            client.close()

if __name__ == '__main__':
    main()
            


