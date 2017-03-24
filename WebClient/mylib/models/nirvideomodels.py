# coding: utf-8
"""
    本部分包含由近红外视频推算血糖浓度等参数的相关模型
"""
import numpy as np
import cv2 as cv
from mylib.utils.videoutils import load_video


class INirVideoModel(object):

    def predict(self, nirvideo_path, *args, **kwargs):
        result = {
            "blood_glucose": 15.5,
            "blood_oxygen": 0.9,
            "heart_rate": 10,
            "body_temperature": 35,
            "blood_pressure": 70,
        }
        image = np.zeros((1024, 1024, 3)).astype('uint8')
        return result, image


class TestNirVideoModel(INirVideoModel):

    def predict(self, nirvideo_path, *args, **kwargs):

        # 返回结果
        result = {
            "blood_glucose": 15.5,
            "blood_oxygen": 0.9,
            "heart_rate": 10,
            "body_temperature": 35,
            "blood_pressure": 70,
        }

        # 载入视频，取视频的第一帧作为图片结果
        nirvideo = load_video(nirvideo_path)
        ret, frame = nirvideo.read()
        if ret:
            return result, frame
        else:
            image = np.zeros((1024, 1024, 3)).astype('uint8')
            return result, image
