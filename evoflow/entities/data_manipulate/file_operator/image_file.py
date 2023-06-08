import os

import cv2
import PIL
from PIL import Image, ImageDraw, ImageFont

from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.Global import Global
from evoflow.Services.OCR.EasyOCREngine import EasyOCREngine
from evoflow.Services.OCR.Result import OCRResult


class ImageFile(File):
    """
    Read and write image files
    """

    def save(self, file_path=None) -> str:
        cv2.imwrite(file_path, self.data)
        return file_path

    def get_info(self) -> str:
        image_name = self.file_path.split(os.sep)[-1]
        image_shape = self.data.shape
        return {"image name": image_name, "image_shape": image_shape}

    def get_texts(self, languages=None, **kwargs):
        """
        try to ocr text from Image
        """
        if languages is None:
            languages = ["en"]
        if Global.ocr_engine is None:
            Global.ocr_engine = EasyOCREngine(languages=languages)
        res = Global.ocr_engine.ocr(self.data, detail=1)
        return res

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_pil(self):
        return PIL.Image.fromarray(self.data)

    def draw(self, ocr_results):
        user_path = f'{os.getenv("userprofile")}/.evoflow/fonts/Noto_Sans_JP/NotoSansJP-Regular.otf'
        data_path = "./data/.evoflow/fonts/Noto_Sans_JP/NotoSansJP-Regular.otf"

        if os.path.isfile(user_path):
            font_file = user_path
        else:
            font_file = data_path

        font = ImageFont.truetype(font_file, 14)
        mat = self.data
        if len(mat.shape) == 2:
            mat = cv2.cvtColor(mat, cv2.COLOR_GRAY2RGB)
        img = Image.fromarray(mat)
        drawer = ImageDraw.Draw(img)
        text_color = "red"
        for ocr_result in ocr_results:
            ocr_result: OCRResult
            top_left = ocr_result.bbox.xmin, ocr_result.bbox.ymin
            bbox = (
                ocr_result.bbox.xmin,
                ocr_result.bbox.ymin,
                ocr_result.bbox.xmax,
                ocr_result.bbox.ymax,
            )
            drawer.text(top_left, ocr_result.text, fill=text_color, font=font)
            drawer.rectangle(bbox, outline="green")
            return img
