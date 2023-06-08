from typing import Iterator

import PIL
import numpy as np
from PIL import Image

from evoflow.controller.log_controller import logger
from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.data_manipulate.file_operator.image_file import ImageFile
from evoflow.Services.abstract_service import AbstractService
from evoflow.Services.ocr.Result import OCRResult


def get_image(data: File):
    pil_image = np.array(Image.open(data.file))
    return pil_image


class OCRService(AbstractService):
    def start(self, **args):
        pass

    def kill(self, **args):
        pass

    def run(self, data: File, **args):
        image = get_image(data)
        result = self.ocr(image, **args)
        return result

    def __init__(self, engine_name="easyocr", languages=None):
        if languages is None:
            languages = ["en", "ja"]
        self.engine = None
        if engine_name == "easyocr":
            # pylint:disable=import-outside-toplevel
            from evoflow.Services.OCR.EasyOCREngine import EasyOCREngine

            self.engine = EasyOCREngine(languages=languages)
        else:
            logger.error("OCR engine name not valid")

        super().__init__()

    def ocr(self, image_file: ImageFile, **args) -> Iterator[OCRResult]:
        """
        OCR text from image.
        :param image_file: Image file format
        """
        if isinstance(image_file, str):
            image = PIL.Image.open(image_file)
        else:
            image = image_file.to_pil()
        results = self.engine.ocr(image, **args)
        return results
