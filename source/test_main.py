
import copy
import time
from PySide6.QtCore import (QObject, Signal)
from PySide6.QtWidgets import (QApplication)
from PySide6.QtGui import (QImage, QPainter, QColor)

import sys
import pathlib


sys.path.append(".")
from source.commands.commands_executor.commands_executor_thread import CommandsExecutorThread
from source.commands.commands_executor.commands_executor_mvc.commands_executor_controller import CommandsExecutorController
from source.commands.commands_vizualizer.commands_vizualizer_controller import CommandsVizualizerController
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

def main():
    
    #Запустим PySide6
    app = QApplication(sys.argv)

    #Загрузим картинку
    # path = pathlib.Path("./assets/fly.jpg")
    path = pathlib.Path("/home/alecksey10/Загрузки/images.jpeg")
    qimage1 = QImage()
    print(path.absolute())
    qimage1.load(str(path.absolute()))
    qimage1.convertTo(QImage.Format.Format_ARGB32)
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

    tmp_filtered_obj = None
    pinned_img_obj = tmp_filtered_obj


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
    def some_handler_on_filter_apply():
        nonlocal tmp_filtered_obj
        tmp_filtered_obj = image_destructurizator_controller.apply_algorithm_to_image(img_obj)
        label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(tmp_filtered_obj))
        pass

    def some_handler_on_filter_apply_to_filtered():
        nonlocal tmp_filtered_obj
        tmp_filtered_obj = image_destructurizator_controller.apply_algorithm_to_image(pinned_img_obj)
        label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(tmp_filtered_obj))
        pass

    def some_handler_pinn_filtered():
        nonlocal tmp_filtered_obj
        nonlocal pinned_img_obj
        pinned_img_obj = tmp_filtered_obj
        pass

    image_destructurizator_controller.apply_filter_signal.connect(some_handler_on_filter_apply)
    image_destructurizator_controller.apply_filter_to_pinned_signal.connect(some_handler_on_filter_apply_to_filtered)
    image_destructurizator_controller.pinn_filtered_image_signal.connect(some_handler_pinn_filtered)



    commands_iterator :CommandsIterator = CommandsIterator([])
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
        nonlocal tmp_filtered_obj
        if(not tmp_filtered_obj):
            return
        commands_generator_controller_base.process_image(tmp_filtered_obj)
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
        


    #-----------------------
    # А здесь сам блок для исполнения команд
    

    
    ex = CommandsExecutorController()    
    
    commands_executor_thread = CommandsExecutorThread()
    commands_executor_thread.start()
    commands_executor_thread.set_commands_iterator(commands_iterator=commands_iterator)

    def commands_executor_thread_start_signal():
        
        #иначе ранее зажатые горячие клавиши могут пересечься с ненужным фукнкционалом. И мышь будет кликаться с одной из зажатых клавишей
        time.sleep(1)
        vizualizated_commands_window.hide()
        transformed_commands = []
        commands_iterator.restart()
        for command in commands_iterator:
            transformed_commands.append(commands_vizualizer_controller.commands_transformator.transform_command(command=command))

        transformed_commands_iterator = CommandsIterator(transformed_commands, width = commands_iterator.width, height = commands_iterator.height)

        commands_executor_thread.set_commands_iterator(transformed_commands_iterator)


        commands_executor_thread.restart_iterations()
    def commands_executor_thread_resume_signal():
        time.sleep(1)
        vizualizated_commands_window.hide()
        commands_executor_thread.resume_iterations()
    def commands_executor_thread_stop_signal():
        vizualizated_commands_window.show()
        commands_executor_thread.stop_iterations()

    def commands_executor_thread_params_changed():
        print(ex.get_executing_time_ms())
        commands_executor_thread.set_delta_time(ex.get_executing_time_ms())

    ex.start_executing_signal.connect(commands_executor_thread_start_signal)
    ex.resume_executing_signal.connect(commands_executor_thread_resume_signal)
    ex.stop_executing_signal.connect(commands_executor_thread_stop_signal)
    ex.params_updated_signal.connect(commands_executor_thread_params_changed)
    
    ex.view.show()    





    sys.exit(app.exec())


if __name__=="__main__":
    main()