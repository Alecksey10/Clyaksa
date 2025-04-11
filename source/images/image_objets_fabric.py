import pathlib
import sys
from PySide6.QtGui import QImage

import numpy as np

sys.path.append('.')
from source.images.color_schemas import ColorSchemas
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor

from source.images.image_object_binary import ImageObjectBinary
from source.images.image_object_ARGB import ImageObjectARGB
from source.images.image_object_base import ImageObjectBase


class ImageObjectsFabric():
    
    @staticmethod
    def argb_from_numpy(arr:np.ndarray)->ImageObjectARGB:
        if(len(arr.shape)!=3):
            raise Exception(f"incorrect arr shape {arr.shape}")
        if(arr.shape[2]!=4):
            raise Exception(f"incorrect arr depth {arr.shape}")
        return ImageObjectARGB(arr.copy())
    
    @staticmethod
    def binary_from_numpy(arr:np.ndarray)->ImageObjectBinary:
        if(len(arr.shape)!=2):
            raise Exception(f"incorrect arr shape {arr.shape}")
        return ImageObjectBinary(arr.copy())
    
    @staticmethod
    def from_numpy_and_color_schemas(arr:np.ndarray, color_schemas:ColorSchemas)->ImageObjectBinary:
        if(color_schemas==ColorSchemas.ARGB):
            return ImageObjectsFabric.argb_from_numpy(arr)
        elif(color_schemas==ColorSchemas.Binary):
            return ImageObjectsFabric.binary_from_numpy(arr)
        else:
            raise Exception("there is no such color_schemas")

def main():
    pass

if __name__=="__main__":
    path = pathlib.Path("./assets/fly.jpg")
    img = QImage()
    print(path.absolute())
    img.load(str(path.absolute()))
    data = ImageObjectsDataExtractor.qimage_to_numpy(image=img)
    print(data.shape)
    img_obj = ImageObjectsFabric.argb_from_numpy(data)
    print(img_obj, img_obj.data.shape, img_obj.get_color_scheme(), img_obj.width)
