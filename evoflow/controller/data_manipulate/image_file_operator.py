#  Copyright (c) 2021. Copyright belongs to evoflow team

import os

import cv2
import numpy as np

from evoflow import logger
from evoflow.controller.data_manipulate.file_operator import FileOperator
from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.data_manipulate.file_operator.ImageFile import ImageFile


def imread(path, flags: int = -1):
    """
    :flags: Default=  cv2.IMREAD_UNCHANGED
    """
    normed_path = os.path.normpath(path)
    mat = cv2.imdecode(np.fromfile(normed_path, dtype=np.uint8), flags)
    if mat is None:
        logger.error(f"Can't read image: {path}")
        raise Exception
    return mat


def imwrite(path, mat):
    image_type = path.split(".")[-1]
    is_success, im_buf_arr = cv2.imencode(".{}".format(image_type), mat)
    im_buf_arr.tofile(path)
    return is_success


cv2.imwrite = imwrite
cv2.imread = imread


class ImageFileOperator(FileOperator):
    """
    File operator with images
    """

    def save(self, file: File, file_path) -> bool:
        return cv2.imwrite(file_path, file.data)

    def read(self, file_path, **args):
        data = cv2.imread(file_path, **args)
        file = ImageFile(file_path=file_path, data=data)
        return file

    @staticmethod
    def supported_file_types():
        return ["jpg", "png", "tiff", "tif"]
