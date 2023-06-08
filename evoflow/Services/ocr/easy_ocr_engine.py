#  Copyright (c) 2021. Copyright belongs to evoflow team

import logging
import os.path
from typing import Iterator
from urllib.error import URLError

import numpy as np

from evoflow import logger
from evoflow.Services.ocr.result import OCRResult

try:
    import easyocr
except ImportError:
    logger.error("Can't import easyocr. Try to install with: pip install easyocr")

MODEL_PATH = "/ocr"


class EasyOCREngine:
    """
    Engine OCR sử dụng thư viện easyocr
    """

    def __init__(self, languages=None):
        if languages is None:
            languages = ["en"]
        try:
            model_storage_directory_evoflow = f'{os.getenv("userprofile")}/.evoflow/ocr'
            model_storage_directory_data = "./data/.evoflow/ocr"
            if os.path.isfile(model_storage_directory_evoflow):
                model_storage_directory = model_storage_directory_evoflow
            else:
                model_storage_directory = model_storage_directory_data
            self.reader = easyocr.Reader(
                languages,
                download_enabled=True,
                model_storage_directory=model_storage_directory,
            )
        except URLError as url_error:
            logger.error("Can't download model, internet blocked")
            raise URLError(
                reason="Can't download model, internet blocked"
            ) from url_error
        logging.info("Initiated EasyOCREngine")

    def ocr(self, image: np.array, detail=0) -> Iterator[OCRResult]:
        """

        :param image: opencv image format
        :param detail:
                0 for simpler output.
                1 for detail output.
        """
        results = self.reader.readtext(np.array(image), detail=detail)

        for i, result in enumerate(results):
            bbox = result[0]
            bbox = [list(map(int, z)) for z in bbox]  # convert np.int32 to int
            res = (bbox, result[1], result[2])
            results[i] = OCRResult(*res)
        return results

    @staticmethod
    def supported_languages() -> Iterator[str]:
        all_lang_list = easyocr.easyocr.all_lang_list
        return all_lang_list
