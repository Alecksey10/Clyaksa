
import copy
from PySide6.QtCore import (QObject, Signal)
from PySide6.QtWidgets import (QApplication)
from PySide6.QtGui import (QImage, QPainter, QColor)

import sys
import pathlib

sys.path.append(".")
from source.commands.press_mouse import PressMouse
from source.commands.release_mouse import ReleaseMouse

from source.commands.move_mouse_global import MoveMouseGlobal
from source.commands.commands_generator_mvc.commands_generator_controller_base import CommandsGeneratorControllerBase

from source.image_filters_algorithms.image_destructurizator_mvc.image_destructurizator_controller import ImageDestructurizatorController
from source.images.image_object_widget import ImageObjectWidget
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objects_visualizer import ImageObjectsVisualizer
from source.images.image_objets_fabric import ImageObjectsFabric

from source.commands.click_mouse import ClickMouse
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.commands.commands_transformator import CommandsTransformator
from source.commands.commands_vizualizer.commands_vizualizer_model import CommandsVizualizerModel
from source.commands.commands_vizualizer.commands_vizualizer_view import CommandsVizualizerView
from source.images.image_object_base import ImageObjectBase
from source.images.utils import Utils

from source.widgets.image_visualizer import ImageVizualizer

class CommandsVizualizerController(QObject):
    #TODO перенагруженный класс:
    # 1) отвечает за визуализацию
    # 2) отвечает за трансформацию
    params_updated_signal = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = CommandsVizualizerView()
        self.model = CommandsVizualizerModel()
        self._commands_iterator:CommandsIterator = CommandsIterator([])
        self._vizualization_canvas:ImageObjectBase = None
        self.commands_transformator = CommandsTransformator(rotation_deg=0, scale=1, shift_x=0, shift_y=0, 
                                                            rotation_center_x=self._commands_iterator.width/2, rotation_center_y=self._commands_iterator.height/2,
                                                              tolerance_rotation=0, tolerance_scale=0, tolerance_shift=0)
    
        self.view.params_updated_signal.connect(self.params_updated_slot)
    
    def set_commands_iterator(self, commands_iterator:CommandsIterator):
        self._commands_iterator = commands_iterator
        self.commands_transformator.rotation_center_x = self.commands_transformator.scale*self._commands_iterator.width/2
        self.commands_transformator.rotation_center_y = self.commands_transformator.scale*self._commands_iterator.height/2

        self.commands_transformator.scale_center_x = 0#self.commands_transformator.scale*self._commands_iterator.width/2
        self.commands_transformator.scale_center_y = 0#self.commands_transformator.scale*self._commands_iterator.height/2
        # self.rebuild_vizualization()
    

    def params_updated_slot(self):
        self.commands_transformator.rotation_deg = self.view.angle_spinbox.value()
        self.commands_transformator.scale = self.view.scale_spinbox.value()
        print(self.commands_transformator)
        self.params_updated_signal.emit()

    def get_commands_visualization(self)->QImage:
        #shift игнорируем при визуализации?...
        width, height = self._commands_iterator.width, self._commands_iterator.height
        width*=self.commands_transformator.scale
        height*=self.commands_transformator.scale
        result_img = QImage(width, height, QImage.Format.Format_RGB32)
        result_img.fill(QColor(0,120,0,1))

        
        self._commands_iterator.restart()
        current_pos = (0, 0)
        #НА ВРЕМЯ ВИЗУАЛИЗАЦИИ ЗАБУДЕМ О СДВИГЕ И ЦЕНТРЕ
        tmp_commands_transformator:CommandsTransformator = copy.copy(self.commands_transformator)
        # tmp_commands_transformator.shift_x = 0
        # tmp_commands_transformator.shift_y = 0
        # tmp_commands_transformator.rotation_center_x = (width/2)
        # tmp_commands_transformator.rotation_center_y = (height/2)
        for command in self._commands_iterator:
            if(isinstance(command,MoveMouseGlobal)):
                current_pos = tmp_commands_transformator.apply_to_point(command.x, command.y)
                current_pos = (current_pos[0] - tmp_commands_transformator.shift_x, current_pos[1] - tmp_commands_transformator.shift_y)
                result_img.setPixelColor(current_pos[0], current_pos[1], QColor(122,122,122,255))
            elif(isinstance(command,ClickMouse)):
                command:ClickMouse
                result_img.setPixelColor(current_pos[0], current_pos[1], QColor(0,0,0,255))
            elif(isinstance(command,PressMouse)):
                result_img.setPixelColor(current_pos[0], current_pos[1], QColor(255,0,0,255))
            elif(isinstance(command,ReleaseMouse)):
                result_img.setPixelColor(current_pos[0], current_pos[1], QColor(0,255,0,255))
            else:
                raise Exception(f"not supported command type {command}")
                
        
        return result_img

    def update_transform_shift(self, x, y):
        self.view.coordinates_label.setText(f"Сдвиг координат x:{x:>5} y:{y:>5}")
        self.commands_transformator.shift_x = x
        self.commands_transformator.shift_y = y

        # width, height = self._commands_iterator.width, self._commands_iterator.height
        # width*=self.commands_transformator.scale
        # height*=self.commands_transformator.scale

        # self.commands_transformator.rotation_center_x = self.commands_transformator.shift_x + width/2
        # self.commands_transformator.rotation_center_y = self.commands_transformator.shift_y + height/2

        # self.commands_transformator.scale_center_x = self.commands_transformator.shift_x + width/2
        # self.commands_transformator.scale_center_y = self.commands_transformator.shift_y + height/2
        

        
def build():
    pass

def main():
    
        #Запустим PySide6
    app = QApplication(sys.argv)

    #Загрузим картинку
    path = pathlib.Path("./assets/fly.jpg")
    qimage1 = QImage()
    print(path.absolute())
    qimage1.load(str(path.absolute()))
    print(qimage1.size(),"width",qimage1.width(), qimage1)
    # преобразуем в numpy
    data = ImageObjectsDataExtractor.qimage_to_numpy(image=qimage1)
    print(data.shape)
    # Преобразуем к нашему формату ImageObjectBase
    img_obj = ImageObjectsFabric.rgba_from_numpy(data)
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
    

    # Виджет генератора
    commands_generator_controller_base = CommandsGeneratorControllerBase()
    commands_generator_controller_base.view.show()

    image_filtered_obj = None


    #На данный момент построено всё, чтобы создавать фильтрованное изображение и команды.
    # Теперь объект с командами надо трансформировать|визуализировать и исполнить.

    commands_vizualizer_controller = CommandsVizualizerController()
    commands_vizualizer_controller.view.setWindowTitle("Контролы")
    commands_vizualizer_controller.view.resize(300, 300)
    commands_vizualizer_controller.view.show()

    vizualizated_commands_window = ImageVizualizer()
    vizualizated_commands_window.drag_and_drop  = True
    vizualizated_commands_window.click_through = False
    # vizualizated_commands_window.always_on_top = False
    vizualizated_commands_window.opacity = 0.4




    #Теперь слоты-заглушки для передачи данных 
    #TODO, по идее нужны мокнутые данные... 
    #Заглушка, как будем применять фильтр к картинке.
    def image_filter_handler():
        nonlocal image_filtered_obj
        image_filtered_obj = image_destructurizator_controller.apply_algorithm_to_image(img_obj)
        label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(image_filtered_obj))
        pass
    image_destructurizator_controller.apply_filter_signal.connect(image_filter_handler)

    commands_iterator :CommandsIterator = None
    #Визуализация команд (вызывается при генерации или изменении параетров)
    def vizualizate_commands(commands_iterator):
            if (commands_iterator == None):
                return
            commands_vizualizer_controller.set_commands_iterator(commands_iterator)
            vizualizated_commands_qimage = commands_vizualizer_controller.get_commands_visualization()
            vizualizated_commands_window.set_image(vizualizated_commands_qimage)
            pass
    
    commands_vizualizer_controller.params_updated_signal.connect(lambda: vizualizate_commands(commands_iterator))
    
    #Заглушка, как будем применять фильтр к картинке.
    def generator_btn_handler():
        nonlocal commands_iterator
        nonlocal image_filtered_obj
        if(not image_filtered_obj):
            return
        commands_generator_controller_base.process_image(image_filtered_obj)
        commands_iterator = commands_generator_controller_base.get_commands_iterator()
        print(commands_iterator, len(commands_iterator))
        vizualizate_commands(commands_iterator)

    commands_generator_controller_base.generate_btn_pressed_signal.connect(generator_btn_handler)

    # Будем захватывать движения от окна визуализации команд, для фиксации сдвигов
    def movement_handler():
        pos = vizualizated_commands_window.get_internal_pos()
        commands_vizualizer_controller.update_transform_shift(pos.x(), pos.y())
        pass
    vizualizated_commands_window.position_changed_signal.connect(movement_handler)
        






    





    sys.exit(app.exec())

if __name__=="__main__":
    main()