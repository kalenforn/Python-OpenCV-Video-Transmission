import struct 
import socket
import traceback
import time
import threading
import os
import numpy as np

from camera import *
from config import DEFAULT_ADDRESS, SAVE_PATH, CONST_TIME, DEFAULT_RESOLUTION, FRAME_QUALITY

class Cilent:

    def __init__(self, address=DEFAULT_ADDRESS, imgPath=SAVE_PATH, resolution=DEFAULT_RESOLUTION, 
                        imgquality=FRAME_QUALITY):
        
        self.__address = address
        self.__savePath = imgPath + '/Picture/'
        self.__quality = imgquality
        try :
            os.mkdir(self.__savePath)
        except:
            pass
        self._video = VideoFrame(resolution)
        self._video.setVideoCapture()
        self._sendData = None

        # 用于保存图片的三个变量
        self.__num = 0
        self.__time = [None, None]

    def _connectting(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.connect(self.__address)
            info = "Socket connected, address: {}".format(self.__address[0])
            write_ordinary_logs(info, "Run_client_log")
            resolution = self._video.getResolution()
            self._socket.send(struct.pack('ii', resolution[0], resolution[1]))
            # print(info)
        except Exception as e: #ConnectionRefusedError
            write_error_logs(e, "Error_client_log")
            # print(e)
        
    def _transmissionEncode(self):
        
        self._video.getVideoFrame()
        self._sendData = self._video.imencode(quality=self.__quality, format='.jpg')
        self._sendData = np.array(self._sendData).tostring()
    
    def _sendFrame(self):
        
        # assert not (self._cilent == self.__resolution == self.__quality == None)

        self._transmissionEncode()  
        # 初次发送一张图片大小
        self._socket.send(struct.pack('i', len(self._sendData))+self._sendData)
        info = "Send image to address:{0}, size:{1}".format(self.__address[0], len(self._sendData))
        write_ordinary_logs(info, "Run_client_log", False)

        while self._video.isOpened():
            try:
                if self._video:
                    threading.Thread(target=self._transmissionEncode(), args=()).start()
                    #self._transmissionEncode()
                """if self._cilent:
                    threading.Thread(target=self._send, args=(self._cilent, struct.pack('i', len(self._sendData))+self._sendData)).start()"""
                self._socket.send(struct.pack('i', len(self._sendData))+self._sendData)
                self._updateTime()
                self.printscreen()
                    # info = "Send image to address:{0}, size:{1}".format(address, len(send_data))
                    # self.__write_ordinary_logs(info, False)
            except Exception as e:
                write_error_logs(e, "Error_client_log")
                info = 'send FPS:{}'.format(self._video.getFrame())
                write_ordinary_logs(info, "Run_client_log")
                self._video.destroyAllWindows()
                return
    
    def _send(self, client, img):
        client.send(img)
                
    # 获取文件数量及文件名
    def getFileCount(self):

        path = os.getcwd()
        os.chdir(self.__savePath)
        lis = os.listdir()
        filecount = len(lis)
        os.chdir(path)
        return filecount, lis
    
    # 删除多余的图片
    def __removeFile(self, filecount, lis):
        
        path = os.getcwd()
        os.chdir(self.__savePath)
        for i in range(self.__num, filecount):
            os.remove(lis[i])
        os.chdir(path)
        info = 'Remove {0} picture'.format(filecount - self.__num)
        write_ordinary_logs(info, "Run_client_log")

    # 重置1分钟存储图片的总数
    def _updateTime(self):

        assert self.__time[0] is not None and self.__time[1] is not None

        _, _, _, _, tm_min, tm_sec, _, _, _ = time.localtime()
        flag = (self.__time[1] == tm_sec and self.__time[0] != tm_min)
        if flag :
            filecount, lis = self.getFileCount()
            info = 'Saved {0} picture in floder:{1}'.format(self.__num, self.__savePath)
            write_ordinary_logs(info, "Run_client_log")
            if filecount > self.__num:
                self.__removeFile(filecount, lis)
            self.__num = 0
            self.__time.clear
            self.__time = [tm_min, tm_sec]

    # 该函数功能如其名，具体实现以后再完善
    def printscreen(self):

        FPS = self._video.getFrame()
        if FPS % CONST_TIME == 0:
            self.__num += 1
            filename = self.__savePath + 'img_{0}.jpg'.format(self.__num)
            self._video.savePicture(filename)

    def run(self):

        self._connectting()
        while True:
            try:
                _, _, _, _, tm_min, tm_sec, _, _, _ = time.localtime()
                self.__time = [tm_min, tm_sec]
                self._sendFrame()
            except Exception as e:
                write_error_logs(e, "Error_client_log")
                return
            finally:
                self._video.destroyAllWindows()



def main():
    try:
        os.mkdir(SAVE_PATH + "/log/")
    except:
        pass
    cilent = Cilent()
    cilent.run()

if __name__ == '__main__':
    main()
