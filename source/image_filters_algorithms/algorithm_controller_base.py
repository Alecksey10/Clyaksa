

from typing import Any
import sys
sys.path.append('.')
from source.image_filters_algorithms.algorithms_registry import AlgorithmsRegistry
from source.images.image_object_base import ImageObjectBase
from source.params_mvc.params_controller import ParamsController
from PySide6.QtCore import Signal
import abc





class AlgorithmBaseController(metaclass=AlgorithmsRegistry):
    #Signal не будет работать, если не наследоваться от QObject
    params_updated_signal = Signal()

    def __init__(self):
        self.params_controller: ParamsController = None
        self.view = None
        self.model = None

    @abc.abstractmethod
    def process_image(img_object:ImageObjectBase) -> ImageObjectBase:
        pass

    @classmethod
    @abc.abstractmethod
    def get_algorithm_name(cls) -> str:
        pass
