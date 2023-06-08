import glob
import json
import os
import pathlib
import urllib
from typing import Iterator

import cv2
import numpy as np
from tqdm import tqdm

import evoflow.Params
from evoflow import logger
from evoflow.controller.data_manipulate.image_file_operator import ImageFileOperator
from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.data_manipulate.file_operator.image_file import ImageFile


def download_poppler():
    try:
        from pyunpack import Archive
    except ImportError:
        logger.error(
            "Can't import pyunpack. Try to install with:\npip install pyunpack"
        )

    poppler_path = f"{os.getenv('userprofile')}/.evoflow/poppler"
    pathlib.Path(poppler_path).mkdir(parents=True, exist_ok=True)
    poppler_file_name = evoflow.Params.POPPLER_URL.rsplit("/", maxsplit=-1)
    opener = urllib.request.URLopener()
    opener.addheader("User-Agent", "evoflow")
    filename, _ = opener.retrieve(
        evoflow.Params.POPPLER_URL, f"{poppler_path}/{poppler_file_name}"
    )
    Archive(filename).extractall(poppler_path)
    os.remove(filename)
    poppler_path = glob.glob(f"{poppler_path}/*/bin")[0]
    return os.path.normpath(poppler_path)


class PdfFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_texts(self):
        page_count = len(self.data.pages)
        texts = []
        for i in range(page_count):
            page = self.data.pages[i]
            text = page.extract_text()
            # text = page_content.encode('utf-8')
            texts.append(text)
        return texts

    def get_info(self) -> str:
        return json.dumps(self.data.metadata, ensure_ascii=False, indent=2)

    def to_images(self, dpi=500) -> Iterator[ImageFile]:
        try:
            # pylint: disable= import-outdide-toplevel
            from pdf2image import convert_from_path
        except ImportError as import_error:
            raise ImportError(
                "Can't import pdf2image. Try to install with: pip install pdf2image"
            ) from import_error

        poppler_paths = glob.glob(f"{os.getenv('userprofile')}/.evoflow/poppler/*/bin")
        if len(poppler_paths) == 0:
            try:
                poppler_path = download_poppler()
            except ValueError as value_error:
                if str(value_error) == "patool not found! Please install patool!":
                    raise ValueError(
                        "patool not found! Please install patool!. \n"
                        "Try to install with: pip install patool"
                    ) from value_error
        else:
            poppler_path = poppler_paths[0]

        pages = convert_from_path(self.file_path, dpi, poppler_path=poppler_path)
        images = []
        for i, page in tqdm(
            enumerate(pages),
            total=len(pages),
            desc=f"Extract image from file: {self.file_path}",
        ):
            image_path = f"{self.file_path}_page_{i}.png"
            page.save(image_path)
            image = ImageFileOperator().read(image_path)
            os.remove(image_path)
            images.append(image)
        return images

    def to_full_image(self, dpi=200) -> ImageFile:
        images = self.to_images(dpi=dpi)
        full_image = images.pop(0)
        for image in images:
            mat1 = full_image.data
            mat2 = image.data
            h_1, w_1 = mat1.shape[:2]
            _, w_2 = mat2.shape[:2]

            if w_1 != w_2:
                mat2 = cv2.resize(mat2, (w_1, int(h_1 * (w_1 / w_2))))

            full_image.data = np.concatenate([mat1, mat2], axis=0)
        return full_image
