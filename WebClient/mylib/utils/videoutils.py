#coding: utf-8
"""
    本部分包含视频读取一系列接口。
"""
import cv2 as cv
from mylib.utils.imageutils import array_to_img, bgr_to_rgb_array


class Video(object):
    """
    opencv VideoCapture 类的封装
    参考：http://docs.opencv.org/3.0-beta/modules/videoio/doc/reading_and_writing_video.html
    """
    propid_dict = {
        'POS_MSEC': 0,
        'POS_FRAMES': 1,
        'FPS': 5,
        'FRAME_COUNT': 7,
    }

    def __init__(self, filename):
        self.video = cv.VideoCapture()
        self.video.open(filename)

    def read(self):
        """
        每调用一次迭代返回一帧图像(PIL Image)
        """
        ret, frame = self.video.read()
        if ret:
            frame = bgr_to_rgb_array(frame)
            frame = array_to_img(frame)
        else:
            frame = None
        return ret, frame

    def get(self, prop_name):
        propid = Video.propid_dict[prop_name]
        return self.video.get(propid)

    def __del__(self):
        self.video.release()


def load_video(path):
    video = Video(path)
    return video