from imagekit.lib import Image, ImageEnhance
from io import BytesIO
from django.core.files import File


def reduce_opacity(im, opacity):
    """Возвращает изображение с уменьшенной непрозрачностью"""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark(imIN, markIN, position, opacity=1):
    """Добавляет водяной знак на изображение"""
    im = Image.open(imIN)
    mark = Image.open(markIN)
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        ratio = min(float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, (int((im.size[0] - w) / 2), int((im.size[1] - h) / 2)))
    else:
        layer.paste(mark, position)
    thumb_io = BytesIO()
    Image.composite(layer, im, layer).save(thumb_io, 'PNG')
    watermarkedImg = File(thumb_io, name=imIN.name)
    im.close()
    mark.close()
    return watermarkedImg
