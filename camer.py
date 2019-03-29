import cv2
import time

from config import DEFAULT_RESOLUTION, SAVE_FPS, SAVE_FORMAT

class VideoFrame:

    def __init__(self, resolution=DEFAULT_RESOLUTION, saveFPS=SAVE_FPS, saveFormat=SAVE_FORMAT):

        # initial all default video config parameter
        self.__resolution = resolution
        self.__saveFPS = saveFPS
        self.__saveFormat = saveFormat

        # initial other value
        self._count_frame = 0
        self._img = None
        self._cap = None
        self._writer = None

    def addFrame(self):
        self._count_frame += 1
    
    def clearFrame(self):
        self._count_frame = 0
    
    # 外部获取帧数的接口
    def getFrame(self):
        return self._count_frame
    
    # 获取帧的接口
    def getImg(self):
        return self._img
    
    def getResolution(self):
        return self.__resolution

    # 初始化摄像头，在server端可不用
    def setVideoCapture(self, num=0):
        self._cap = cv2.VideoCapture(num)
    
    # 初始化写的单位，在client端可以不用
    def setVideoWriter(self, savefile):
        self._writer = cv2.VideoWriter(savefile, self.__saveFormat, self.__saveFPS , self.__resolution)
    
    def imdecode(self, buffer, flags=1):
        return cv2.imdecode(buffer, flags)
    
    # 编码，只负责编img变量的函数，在socket传输中还需要加工
    def imencode(self, quality=12, format='.jpg'):

        assert len(self._img) != 0

        params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        img = cv2.resize(self._img,self.__resolution)
        return cv2.imencode(format, img, params)[1]

    # 获取视频帧
    def getVideoFrame(self):

        assert self._cap != None

        # 帧存储在保护变量img里
        self._img = self._cap.read()[1]
        # 帧数加1
        # print(self._img)
        self.addFrame()
        #return self.getImg()

    def writeVideo(self, buffer):

        assert self._writer != None

        _, _, _, tm_hour, tm_min, tm_sec, _, _, _ = time.localtime()
        cv2.putText(buffer, str(tm_hour) + ":" + str(tm_min) + ":" + str(tm_sec), (10, 20), 
                        cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA)
        self._writer.write(buffer)
        self.addFrame()
    
    def savePicture(self, filename):
        cv2.imwrite(filename, self._img)

    # 释放writer,保存视频
    def saveRelease(self):

        assert self._writer != None

        self._writer.release()
        self._writer = None

    def showVidoe(self, buffer, windowsName="Video"):
        cv2.imshow(windowsName, buffer)

    # 防止程序意外bug使数据丢失
    def destroyAllWindows(self):
        if self._cap != None:
            self._cap.release()
        if self._writer != None:
            self._writer.release()
        cv2.destroyAllWindows()

    def waitetime(self, time):
        return cv2.waitKey(time)



    
