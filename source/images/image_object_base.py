import numpy as np
import abc

from source.images.color_schemas import ColorSchemas


class ImageObjectBase(abc.ABC):
    
    def __init__(self):
        self._width = None
        self._height = None

    @property
    def width(self)->int:
        return self._width

    @property
    def height(self)->int:
        return self._height

    @property
    @abc.abstractmethod
    def shape(self):
        pass

    @abc.abstractmethod
    def get_color_scheme()->ColorSchemas:
        pass

    @abc.abstractmethod
    def get_as_numpy()->np.ndarray:
        pass