import struct 
import socket
import traceback
import time
import os
import numpy as np

from camer import VideoFrame
from config import DEFAULT_ADDRESS, SAVE_PATH, CONST_TIME

class Server:
    
    def __init__(self, address=DEFAULT_ADDRESS, imgPath=SAVE_PATH):
        
        self.__address = address
        self.__savePath = imgPath + '/Picture/'
        try :
            os.mkdir(self.__savePath)
        except:
            pass
        self._video = self._cilent = self.__resolution = self.__quality = None
        self._userAddress = None

        self._initialSocket()

        # 用于保存图片的三个变量
        self.__num = 0
        self.__time = [None, None]

        # self.__initialConfig()

    # 初始化服务器端的socket
    def _initialSocket(self):

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._socket.bind(self.__address)
        self._socket.listen(5)
        info = "Socket Create in ip: {0}, port:{1}".format(self.__address[0], self.__address[1])
        self._write_ordinary_logs(info)

    # 初始化所需要的配置:video reloution，img quality, video reader
    def _initialConfig(self):

        buffer = self._cilent.recv(12)
        # print("Receive data:", buffer)
        buffer = struct.unpack('iii', buffer)
        info = "Receive data from: {0}, Size:{1}".format(self._userAddress, len(buffer))
        self._write_ordinary_logs(info, False)
        # print(buffer)

        self.__num = 0
        self.__time = [None, None]

        if buffer[0] != 0:
            self.__resolution = (buffer[1], buffer[2])
            self.__quality = buffer[0]
            #self.__transSize = buffer[0]
            self._video = VideoFrame(resolution=self.__resolution)
            self._video.setVideoCapture(0)
            info = 'Open camera'
            self._write_ordinary_logs(info)
    
    def _write_error_logs(self, e):

        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        with open("Error_log_server", 'a+') as f:
            f.writelines("\n*********************************************************************\n")
            f.write("Error:time:{0:4d}/{1:2d}/{2:2d},{3:2d}:{4:2d}:{5:2d}\\\\\n:{6}".format(tm_year, 
                        tm_mon, tm_mday, tm_hour, tm_min, tm_sec, traceback.format_exc()))
            f.writelines("*********************************************************************\n")
    
    def _write_ordinary_logs(self, info, head=True):
        
        assert isinstance(info, str)
        assert isinstance(head, bool)

        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        with open('Run_log_server', 'a+') as f:
            if head :
                f.writelines("\n\n*********************************************************************\n")
            f.write("INFO:time:{0:4d}/{1:2d}/{2:2d},{3:2d}:{4:2d}:{5:2d}\\\\{6}".format(tm_year, 
                        tm_mon, tm_mday, tm_hour, tm_min, tm_sec, info + "\n"))
    
    def run(self):

        while True :
            try:
                print("Waitting connect:")
                self._cilent, address = self._socket.accept()
                self._userAddress = address
                print("Creating connect")
                self._initialConfig()
                _, _, _, _, tm_min, tm_sec, _, _, _ = time.localtime()
                self.__time = [tm_min, tm_sec]
                # print("Initial config")
                self._sendVideoFrame(address)
            except Exception as e:
                self._write_error_logs(e)
            finally:
                #self._socket.close()
                if self._cilent:
                    self._cilent.close()

    # 因为camer类里边的编码器的功能只是用来将采集来的图片编码成jpg格式的压缩图片，这种编码的图片并不适合socket传输，故而再经过一次深层次编码
    def _transmissionEncode(self):
        self._video.getVideoFrame()
        send_data = self._video.imencode(quality=self.__quality, format='.jpg')
        send_data = np.array(send_data).tostring()
        return send_data
    
    # 发送图片帧
    def _sendVideoFrame(self, address):
        
        assert not (self._cilent == self.__resolution == self.__quality == None)

        send_data = self._transmissionEncode()  
        # 初次发送一张图片大小
        self._cilent.send(struct.pack('i', len(send_data))+send_data)
        info = "Send image to address:{0}, size:{1}".format(address, len(send_data))
        self._write_ordinary_logs(info, False)

        while True:
            try:
                self._cilent.send(struct.pack('i', len(send_data))+send_data)
                self._updateTime()
                self.printscreen()
                if self._video:
                    send_data = self._transmissionEncode()
                    # info = "Send image to address:{0}, size:{1}".format(address, len(send_data))
                    # self.__write_ordinary_logs(info, False)
            except Exception as e:
                self._write_error_logs(e)
                info = 'send FPS:{}'.format(self._video.getFrame())
                self._write_ordinary_logs(info)
                self._video.destroyAllWindows()
                return 
                
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
        info = 'Remove {0} picture'.format(filecount - self.__num)
        os.chdir(path)

    # 重置1分钟存储图片的总数
    def _updateTime(self):

        assert self.__time[0] is not None and self.__time[1] is not None

        _, _, _, _, tm_min, tm_sec, _, _, _ = time.localtime()
        flag = (self.__time[1] == tm_sec and self.__time[0] != tm_min)
        if flag :
            filecount, lis = self.getFileCount()
            info = 'Saved {0} picture in floder:{1}'.format(self.__num, self.__savePath)
            self._write_ordinary_logs(info)
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

def main():
    server = Server()
    while True:
        try:
            server.run()
        except Exception as e:
            server._write_error_logs(e)

if __name__ == '__main__':
    main()

