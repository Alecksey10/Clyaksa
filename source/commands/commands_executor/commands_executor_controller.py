from PySide6.QtCore import Signal, QObject

from source.commands.commands_executor.commands_executor_model import CommandsExecutorModel
from source.commands.commands_executor.commands_executor_view import CommandsExecutorView

class CommandsExecutorController(QObject):
    start_executing_clicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = CommandsExecutorView()
        self.model = CommandsExecutorModel()

    

    