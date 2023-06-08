import numpy as np


class Bounding:
    def __init__(self, bbox):
        bbox = np.array(bbox)
        self.bbox = bbox
        self.xmin = min(bbox[:, 0])
        self.xmax = max(bbox[:, 0])
        self.ymin = min(bbox[:, 1])
        self.ymax = max(bbox[:, 1])

    def get_center(self):
        center = (self.xmax + self.xmin) / 2, (self.ymax + self.ymin) / 2
        return np.array(center)

    def compute_distance(self, bbox):
        _c1 = self.get_center()
        _c2 = bbox.get_center()
        distance = (_c1 - _c2) ** 2
        return sum(distance) ** (1 / 2)

    def shift_x(self, pixcel):
        self.bbox[:, 0] += pixcel
        self.xmin += pixcel
        self.xmax += pixcel

    def shift_y(self, pixcel):
        pass


# pylint: disable=too-few-public-methods
class OCRResult:
    def __init__(self, bbox, text, confidence):
        self.bbox = Bounding(bbox)
        self.text = text
        self.confidence = confidence

    def __repr__(self):
        return f"{self.text}, {self.confidence}"
