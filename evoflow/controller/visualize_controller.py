from PIL import ImageDraw
from PIL import ImageFont


def draw_boxes(image, bounds, color="yellow", width=2):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("data/HachiMaruPop-Regular.ttf", 32)
    for bound in bounds:
        p_0, p_1, p_2, p_3 = bound[0]
        text = bound[1]
        draw.line([*p_0, *p_1, *p_2, *p_3, *p_0], fill=color, width=width)
        draw.text(p_0, text, (255, 0, 0), font=font)
    return image
