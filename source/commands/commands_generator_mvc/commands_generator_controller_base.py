from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import Signal
import sys
sys.path.append('.')
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






if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = CommandsGeneratorControllerBase()
    controller.view.show()
    sys.exit(app.exec())