

import abc

import sys

sys.path.append(".")
from source.commands.press_mouse import PressMouse
from source.commands.release_mouse import ReleaseMouse

from typing import List
from source.commands.click_mouse import ClickMouse
from source.commands.command_base import CommandBase
from source.commands.commands_generator.commands_generator_base import CommandsGeneratorBase
from source.commands.commands_generator.commands_generator_intensivity_mvc.commands_generator_intensivity_model import CommandsGeneratorIntensivityModel
from source.commands.commands_generator.commands_generator_intensivity_mvc.commands_generator_intensivity_view import CommandsGeneratorIntensivityView
# from source.commands.commands_generator_mvc.commands_generator_controller_base import CommandsGeneratorControllerBase
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.commands.mouse.button import Button
from source.commands.move_mouse_global import MoveMouseGlobal
# from source.image_filters_algorithms.image_destructurizator_mvc.image_destructurizator_controller import ImageDestructurizatorController
from source.images.color_schemas import ColorSchemas
from source.images.image_object_base import ImageObjectBase



import pathlib

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QComboBox, QCheckBox, QApplication, QLabel
)
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QImage, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt, QPoint

from PySide6.QtCore import QObject


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


class CommandsGeneratorIntensivityController(CommandsGeneratorBase):
    
    def __init__(self):
        super().__init__()
        self.model = CommandsGeneratorIntensivityModel()
        self.view = CommandsGeneratorIntensivityView() 
        self.img_object = None

    def process_image_object(self, img_object:ImageObjectBase):
        if(img_object.get_color_scheme()!=ColorSchemas.Binary):
            raise Exception(f"cannot handle such color schema {img_object.get_color_scheme()} {CommandsGeneratorIntensivityController}")
        self.img_object = img_object
        pass

    def get_commands_iterator(self) -> CommandsIterator:
        width, height = self.img_object.width, self.img_object.height
        commands:List[CommandBase] = []

        threshold =self.view.intensity_spin.value()
        #на skip и checkpoints тоже
        skip = self.view.trim_commands_checkbox.isChecked()
        checkpoints = self.view.checkpoints_checkbox.isChecked()
        
        # Пока на радиус всё равно
        radius = self.view.min_distance_spin.value()

        #Можно оптимизировать...
        img_np = self.img_object.get_as_numpy()
        
        if(not skip):
            for i in range(0, height):
                for j in range(0, width):
                    if(img_np[i,j]<threshold):
                        commands.append(MoveMouseGlobal(x=j, y=i))
                        commands.append(ClickMouse(button=Button.left))
        elif(skip):
            #Иначе будем закрашивать через зажатие мыши и просто передвижение. 
            state = 'searching_start'
            for i in range(0, height):
                for j in range(0, width):
                    if(img_np[i,j]<threshold):
                        if(state=='searching_start'):
                            commands.append(MoveMouseGlobal(x=j, y=i))
                            commands.append(PressMouse(button=Button.left))
                            state = "searching_end"
                    else:
                        if(state=="searching_end"):
                            commands.append(MoveMouseGlobal(x=j-1, y=i))
                            commands.append(ReleaseMouse(button=Button.left))
                            state = "searching_start"
                
                if(state=="searching_end"):
                    commands.append(MoveMouseGlobal(x=width-1, y=i))
                    commands.append(ReleaseMouse(button=Button.left))
                    state = "searching_start"


        
        return CommandsIterator(commands=commands, width=self.img_object.width, height=self.img_object.height)


    @classmethod
    def get_generator_name(cls) -> str:
        return "intensivity commands generator"
    

#По идее проверять не надо, он должен проявляться прямо в commands_generator_controller_base
# def main():
#     #Запустим PySide6
#     app = QApplication(sys.argv)

#     #Загрузим картинку
#     path = pathlib.Path("./assets/fly.jpg")
#     qimage1 = QImage()
#     print(path.absolute())
#     qimage1.load(str(path.absolute()))
#     print(qimage1.size(),"width",qimage1.width(), qimage1)
#     # преобразуем в numpy
#     data = ImageObjectsDataExtractor.qimage_to_numpy(image=qimage1)
#     print(data.shape)
#     # Преобразуем к нашему формату ImageObjectBase
#     img_obj = ImageObjectsFabric.argb_from_numpy(data)
#     print(img_obj, img_obj.data.shape, img_obj.get_color_scheme(), img_obj.width)


#     # Построим контроллер, на сигналы которого будем преобразовывать картинки. 
#     image_destructurizator_controller = ImageDestructurizatorController(img_obj.width, img_obj.height)
#     image_destructurizator_controller.view.show()
    
#     # Основная картинка
#     label = ImageObjectWidget()
#     label.set_image(qimage1)
#     label.show()

#     label2 = ImageObjectWidget()
#     label2.set_image(qimage1)
#     label2.show()
    

#     # Виджет генератора
#     commands_generator_controller_base = CommandsGeneratorControllerBase()
#     commands_generator_controller_base.view.show()

#     image_filtered_obj = None

#     #Заглушка, как будем применять фильтр к картинке.
#     def image_filter_handler():
#         nonlocal image_filtered_obj
#         image_filtered_obj = image_destructurizator_controller.apply_algorithm_to_image(img_obj)
#         label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(image_filtered_obj))
#         pass

#     #Заглушка, как будем применять фильтр к картинке.
#     def generator_btn_handler():
#         nonlocal image_filtered_obj
#         if(not image_filtered_obj):
#             return
#         commands_generator_controller_base.process_image(image_filtered_obj)
#         commands = commands_generator_controller_base.get_commands_iterator()
#         print(commands, len(commands))


#     image_destructurizator_controller.apply_filter_signal.connect(image_filter_handler)

#     commands_generator_controller_base.generate_btn_pressed_signal.connect(generator_btn_handler)



#     sys.exit(app.exec())
    
#     pass


# if __name__=="__main__":
#     main()