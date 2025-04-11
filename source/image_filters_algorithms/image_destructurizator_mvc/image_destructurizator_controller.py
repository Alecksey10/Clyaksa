

import pathlib
import sys

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QComboBox, QCheckBox, QApplication, QLabel
)
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QImage, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt, QPoint

from PySide6.QtCore import QObject

sys.path.append(".")
from source.images.utils import Utils

from source.images.image_object_base import ImageObjectBase
from source.images.image_object_widget import ImageObjectWidget
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objects_visualizer import ImageObjectsVisualizer
from source.images.image_objets_fabric import ImageObjectsFabric

from source.image_filters_algorithms.algorithms_registry import AlgorithmsRegistry
from source.image_filters_algorithms.image_destructurizator_mvc.image_destructurizator_view import ImageDestructurizatorView
from source.params.stricts_loader import StrictsLoader
from source.params.params_scheme_base import ParamsSchemeBase
from source.params_mvc.params_controller import ParamsController
from source.image_filters_algorithms.algorithm_controller_base import AlgorithmBaseController
from source.image_filters_algorithms import *
from PySide6.QtCore import Signal


class ImageDestructurizatorController(QObject):

    apply_filter_signal = Signal()

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_algorithm_controller:AlgorithmBaseController = None
        
        # params_scheme_base:ParamsSchemeBase = StrictsLoader.load_fields_scheme_from_json(pathlib.Path("./source/image_filters_algorithms/image_destructurizator_mvc/stricts.json"))
        # self.params_controller = ParamsController(params_scheme_base)
        

        self.init_ui(width, height)
        self.view.combo.setCurrentIndex(0)
        self.algorithm_changed_slot()
        

    def init_ui(self, width, height):
        
        self.view = ImageDestructurizatorView(width, height)
        combo:QComboBox = self.view.combo
        #TODO Пока так, организовать регистарцию в каком-нибудь классе, а затем сборы?
        # self.current_algorithm_controller:AlgorithmBaseController = AlgorithmThresholdOneController()
        # print(self.current_algorithm_controller.params_controller.params_scheme.fields)
        algorithms_classes = AlgorithmsRegistry.get_registered_algorithms_names()

        self.view.combo.addItems(algorithms_classes)
        combo.currentIndexChanged.connect(self.algorithm_changed_slot)

        algorithm_container = self.view.algorithm_container
        algorithm_container.setLayout(QVBoxLayout())


        self.view.layout().addWidget(QLabel("Выберите фильтр:"))
        self.view.layout().addWidget(self.view.combo)
        self.view.layout().addWidget(self.view.algorithm_container)
        self.view.layout().addWidget(self.view.checkbox)
        self.view.layout().addWidget(QLabel("Ширина"))
        self.view.layout().addWidget(self.view.width_spin)
        self.view.layout().addWidget(QLabel("Высота"))
        self.view.layout().addWidget(self.view.height_spin)
        self.view.layout().addWidget(self.view.button)        


        # Сигналы (можно привязать обработчики)
        self.view.button.clicked.connect(self.apply_filter_slot)
        # self.view.apply_filter_signal.connect(self.apply_filter_slot)

    def reinit_algorithm(self, algorithm_base_controller: AlgorithmBaseController):
        self.current_algorithm_controller = algorithm_base_controller

        algorithm_container:QWidget = self.view.algorithm_container

        while  algorithm_container.layout().count():
            item =  algorithm_container.layout().takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        
        algorithm_container.layout().addWidget(self.current_algorithm_controller.params_controller.view)


    def algorithm_changed_slot(self):
        text = self.view.combo.currentText()
        for cls in AlgorithmsRegistry.get_registered_algorithms():
            if(text==cls.get_algorithm_name()):
                self.reinit_algorithm(cls())

    def apply_algorithm_to_image(self, img_obj:ImageObjectBase)->ImageObjectBase:
        img_np = img_obj.get_as_numpy()
        img_np = Utils.resize_array(img_np, self.view.width_spin.value(), self.view.height_spin.value())
        result_img:ImageObjectBase = self.current_algorithm_controller.process_image(ImageObjectsFabric.from_numpy_and_color_schemas(img_np, img_obj.get_color_scheme()))
        return result_img

    def apply_filter_slot(self):
        print("self filter applied")
        self.apply_filter_signal.emit()
        #А также применим фильтры в рамках данного виджета
        



def main():
    #Запустим PySide6
    app = QApplication(sys.argv)

    #Загрузим картинку
    path = pathlib.Path("./assets/cherv.jpg")
    qimage1 = QImage()
    print(path.absolute())
    qimage1.load(str(path.absolute()))
    print(qimage1.size(), qimage1)
    # преобразуем в numpy
    data = ImageObjectsDataExtractor.qimage_to_numpy(image=qimage1)
    print(data.shape)
    # Преобразуем к нашему формату ImageObjectBase
    img_obj = ImageObjectsFabric.argb_from_numpy(data)
    print(img_obj, img_obj.data.shape, img_obj.get_color_scheme(), img_obj.width)


    # Построим контроллер, на сигналы которого будем преобразовывать картинки. 
    image_destructurizator_controller = ImageDestructurizatorController(img_obj.width, img_obj.height)
    image_destructurizator_controller.view.show()
    
    # Основная картинка
    label = ImageObjectWidget()
    label.set_image(qimage1)
    label.show()

    label2 = ImageObjectWidget()
    label2.set_image(qimage1)
    label2.show()
    #Заглушка, как будем применять фильтр к картинке.
    def some_handler():
        qimage_filtered = image_destructurizator_controller.apply_algorithm_to_image(img_obj)
        label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(qimage_filtered))
        pass

    image_destructurizator_controller.apply_filter_signal.connect(some_handler)

    sys.exit(app.exec())
    
    pass

if __name__=="__main__":
    main()