# coding=gbk
"""
author(����): Channing Xie(л�)
time(ʱ��): 2020/6/18 6:49
filename(�ļ���): image_io_channing.py
function description(��������):
...
"""
import numpy as np
import cv2


def read_image(path: str, image_type=1):
    """
    ��ȡһ��numpyͼ��
    :param path: ͼ��·��
    :param image_type: 1����rgb��0����gray��-1����rgbd��
    :return:
    """
    assert image_type in [-1, 0, 1]
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), image_type)
    return image


def save_image(path: str, image: np.ndarray, image_type='.bmp'):
    """
    д��һ��numpyͼ��
    :param path: �洢·��
    :param image: ��Ҫ���洢��ͼ��
    :param image_type: �洢��ͼ�����ͣ���png��jpg��
    :return:
    """
    assert image_type in ['.bmp', '.png', '.jpg', '.jpeg']
    cv2.imencode(image_type, image)[1].tofile(path)

