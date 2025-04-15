

import pathlib
import sys

sys.path.append(".")

from source.images.color_schemas import ColorSchemas
from source.images.image_objets_fabric import ImageObjectsFabric
from source.images.image_object_base import ImageObjectBase
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objects_visualizer import ImageObjectsVisualizer
from source.params.params_scheme_base import ParamsSchemeBase
from source.params.stricts_loader import StrictsLoader
from source.params_mvc.params_controller import ParamsController
from PySide6.QtCore import Signal
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from source.image_filters_algorithms.algorithm_controller_base import AlgorithmBaseController
import numpy as np
from skimage import color, filters

class AlgorithmContour(AlgorithmBaseController):

    params_updated_signal = Signal()

    def __init__(self):
        params_scheme_base:ParamsSchemeBase = StrictsLoader.load_fields_scheme_from_json(pathlib.Path("./source/image_filters_algorithms/algorithm_contour/stricts.json"))
        self.params_controller = ParamsController(params_scheme_base)
    
    def process_image(self, img_object:ImageObjectBase) -> ImageObjectBase:
        data:np.ndarray = ImageObjectsFabric.from_any_to_color_schema(img_object, ColorSchemas.Binary).get_as_numpy()

        edges = filters.sobel(data)
        coef = self.params_controller.get_value("mulf_coef")
        
        binary = -((np.clip(edges*coef*255, 0, 255)).astype(np.uint8)-255)
        return ImageObjectsFabric.binary_from_numpy(binary)
    
    @classmethod
    def get_algorithm_name(cls):
        return "algorithms contour"

def main():
    pass

if __name__=="__main__":
    # 1) load image
    img = QImage()
    img.load(str(pathlib.Path("assets/img1.png").absolute()))

    img_np = ImageObjectsDataExtractor.qimage_to_numpy(img)
    
    

    #start pyside
    app = QApplication(sys.argv)

    algorithm_controller = AlgorithmContour()
    algorithm_controller.params_controller.view.show()
    # filtered:ImageObjectBase = algorithm_controller.process_image()

    sys.exit(app.exec())
