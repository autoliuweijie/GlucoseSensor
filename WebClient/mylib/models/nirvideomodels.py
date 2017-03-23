# coding: utf-8
"""
    本部分包含由近红外视频推算血糖浓度等参数的相关模型
"""
import numpy as np

class INirVideoModel(object):

    def predict(self, nirvideo, *args, **kwargs):
        result = {
            "blood_glucose": 15.5,
            "blood_oxygen": 0.9,
            "heart_rate": 10,
            "body_temperature": 35,
            "blood_pressure": 70,
        }
        image = np.zeros((1024, 1024, 3)).astype('uint8')
        return result, image