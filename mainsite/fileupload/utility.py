# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File Name：   utility
  Description : MiniMES Company
  Author :    Karo Lin
  date：     2022/10/19
  Copyright follow MIT definitions.
-------------------------------------------------
  Change Activity:
          2022/10/19:
-------------------------------------------------
"""
__author__ = 'Karo Lin'

import uuid
import os

# Use uuid as file name.
from io import BytesIO

from PIL import Image, ExifTags
from django.core.files import File


# 使用不重複編碼為檔名儲存圖片
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('icons', filename)


# A function to return human-readable size from bytes size.
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# 壓縮並旋轉Icon檔案，使得方向正確以及避免伺服器空間耗盡。(ImageField use only)
def make_thumbnail(image, file_name, size=(500, 500)):
    """Makes thumbnails of given size from given image"""
    pil_image = Image.open(image)
    w, h = pil_image.size
    print('\033[93m*** Original image scale W:%spx, H:%spx.\033[00m' % (w, h))
    origin_image_size = image.getbuffer().nbytes
    print('\033[93m*** Original Image Size: %s\033[00m' % sizeof_fmt(origin_image_size))
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(pil_image._getexif().items())
        if exif[orientation] == 3:
            pil_image = pil_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            pil_image = pil_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            pil_image = pil_image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
    pil_image.thumbnail(size)  # resize image
    w, h = pil_image.size
    print('\033[93m*** New image scale W:%spx, H:%spx.\033[00m' % (w, h))
    if pil_image.mode in ("RGBA", "P"):
        pil_image = pil_image.convert("RGB")  # convert mode
    thumb_io = BytesIO()  # create a BytesIO object
    pil_image.save(thumb_io, 'JPEG', quality=85)  # save image to BytesIO object
    thumbnail = File(thumb_io, name=file_name)  # create a django friendly File object
    new_size = int(thumbnail.size)
    print('\033[93m*** New Image Size: %s\033[00m' % sizeof_fmt(new_size))
    return thumbnail
