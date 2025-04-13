from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import Signal, QObject
import sys
import pathlib
sys.path.append('.')
from source.image_filters_algorithms.image_destructurizator_mvc.image_destructurizator_controller import ImageDestructurizatorController
from source.images.image_object_widget import ImageObjectWidget
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objects_visualizer import ImageObjectsVisualizer
from source.images.image_objets_fabric import ImageObjectsFabric

from source.images.image_object_base import ImageObjectBase
from source.commands.commands_generator.commands_generator_registry import CommandsGeneratorRegistry
from source.commands.commands_generator_mvc.commands_generator_model_base import CommandsGeneratorModelBase
from source.commands.commands_generator_mvc.commands_generator_view_base import CommandsGeneratorViewBase
from source.commands.commands_generator.commands_generator_base import CommandsGeneratorBase
from source.commands import commands_generator


class CommandsGeneratorControllerBase(QObject):
    
    generate_btn_pressed_signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = CommandsGeneratorModelBase()
        self.current_generator_controlller:CommandsGeneratorBase = None
        
        self.view = self._build_view()
        self.view.generator_changed_signal.connect(self.reinit_generator)
        self.view.generate_btn_pressed_view_signal.connect(self.generate_btn_pressed_slot)
        self.view.combobox.setCurrentIndex(0)
        self.reinit_generator()

    def _build_view(self):
        view = CommandsGeneratorViewBase()
        generators_names = CommandsGeneratorRegistry.get_registered_generators_names()
        view.combobox.addItems(generators_names)
        return view
    
    def reinit_generator(self):
        current_generator_name = self.view.combobox.currentText()
        for cls in CommandsGeneratorRegistry.get_registered_generators():
            cls:CommandsGeneratorBase
            if(cls.get_generator_name()==current_generator_name):
                self.current_generator_controlller = cls()
                self.view.set_settings_widget(self.current_generator_controlller.view)
    
    def generate_btn_pressed_slot(self):
        print("generate btn pressed slot")
        self.generate_btn_pressed_signal.emit()

    def get_commands_iterator(self):
        return self.current_generator_controlller.get_commands_iterator()
        
    def process_image(self, image:ImageObjectBase):
        return self.current_generator_controlller.process_image_object(image)





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
    

    # Виджет генератора
    commands_generator_controller_base = CommandsGeneratorControllerBase()
    commands_generator_controller_base.view.show()

    image_filtered_obj = None

    #Заглушка, как будем применять фильтр к картинке.
    def image_filter_handler():
        nonlocal image_filtered_obj
        image_filtered_obj = image_destructurizator_controller.apply_algorithm_to_image(img_obj)
        label2.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(image_filtered_obj))
        pass

    #Заглушка, как будем применять фильтр к картинке.
    def generator_btn_handler():
        nonlocal image_filtered_obj
        if(not image_filtered_obj):
            return
        commands_generator_controller_base.process_image(image_filtered_obj)
        commands = commands_generator_controller_base.get_commands_iterator()
        print(commands, len(commands))


    image_destructurizator_controller.apply_filter_signal.connect(image_filter_handler)

    commands_generator_controller_base.generate_btn_pressed_signal.connect(generator_btn_handler)



    sys.exit(app.exec())
    
    pass


if __name__=="__main__":
    main()