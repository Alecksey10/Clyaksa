import pathlib
import numpy as np

from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap

import sys

sys.path.append(".")
from source.images.image_object_widget import ImageObjectWidget

from source.images.color_schemas import ColorSchemas
from source.images.image_object_base import ImageObjectBase
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objets_fabric import ImageObjectsFabric

class ImageObjectsVisualizer():
    @staticmethod
    def convert_image_obj_to_qimage(image_object_base:ImageObjectBase) -> QImage:
        """
        Преобразует ndarray (H, W, 4) в QImage с форматом ARGB32.

        arr: numpy.ndarray с dtype=uint8, shape=(H, W, 4) — ожидается порядок [R, G, B, A]

        Возвращает: QImage
        """
        if(image_object_base.get_color_scheme()==ColorSchemas.ARGB):
            return ImageObjectsVisualizer.convert_numpy_from_argb_to_qimage(image_object_base.get_as_numpy())

        if(image_object_base.get_color_scheme()==ColorSchemas.Binary):
            return ImageObjectsVisualizer.convert_numpy_from_binary_to_qimage(image_object_base.get_as_numpy())


    @staticmethod
    def convert_numpy_from_argb_to_qimage(arr):
        if arr.dtype != np.uint8 or arr.ndim != 3 or arr.shape[2] != 4:
            raise ValueError("Error ndarray с shape=(H, W, 4) и dtype=uint8")

        h, w, _ = arr.shape

        # Переставляем каналы с RGBA → ARGB (QImage.Format_ARGB32 ожидает BGRA-порядок)
        argb_arr = np.empty((h, w, 4), dtype=np.uint8)
        argb_arr[..., 0] = arr[..., 2]  # B
        argb_arr[..., 1] = arr[..., 1]  # G
        argb_arr[..., 2] = arr[..., 0]  # R
        argb_arr[..., 3] = arr[..., 3]  # A

        # Создаём QImage — нужно указать strides
        qimg = QImage(
            argb_arr.data, w, h, argb_arr.strides[0],
            QImage.Format.Format_ARGB32
        ).copy()  

        return qimg
    
    def convert_numpy_from_binary_to_qimage(arr: np.ndarray) -> QImage:
        if arr.dtype != np.uint8 or arr.ndim != 2:
            raise ValueError("Error 2D numpy.ndarray с dtype=uint8")

        h, w = arr.shape
        return QImage(
            arr.data, w, h, arr.strides[0],
            QImage.Format.Format_Grayscale8
        ).convertToFormat(QImage.Format.Format_ARGB32)

    

if __name__=="__main__":
    path = pathlib.Path("./assets/fly.jpg")
    qimage1 = QImage()
    print(path.absolute())
    qimage1.load(str(path.absolute()))
    data = ImageObjectsDataExtractor.qimage_to_numpy(image=qimage1)
    print(data.shape)
    img_obj = ImageObjectsFabric.rgba_from_numpy(data)
    print(img_obj, img_obj.data.shape, img_obj.get_color_scheme(), img_obj.width)


    qimage2 = ImageObjectsVisualizer.convert_image_obj_to_qimage(img_obj)

    #теперь визуализируем (должны быть 2 одинаковые картинки. )
    app = QApplication(sys.argv)

    label = ImageObjectWidget()
    label.set_image(qimage1)
    label.show()

    label2 = ImageObjectWidget()
    label2.set_image(qimage2)
    label2.show()

    sys.exit(app.exec())
