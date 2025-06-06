import numpy as np
import abc

import sys
sys.path.append('.')

from source.images.color_schemas import ColorSchemas
from source.images.image_object_base import ImageObjectBase


class ImageObjectBinary(ImageObjectBase):
    
    def __init__(self, numpy_data:np.ndarray):
        self._height, self._width = numpy_data.shape
        self.data = numpy_data

    @property
    def shape(self):
        return self.data.shape 

    def get_color_scheme(self)->ColorSchemas:
        return ColorSchemas.Binary

    def get_as_numpy(self)->np.ndarray:
        return self.data