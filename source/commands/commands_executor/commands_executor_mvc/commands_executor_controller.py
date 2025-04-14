from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QGridLayout


import sys



sys.path.append(".")

from source.commands.move_mouse_global import MoveMouseGlobal
from source.commands.commands_executor.commands_executor_thread import CommandsExecutorThread
from source.shortcats.shortcat_matcher import ShortcatMatcher
from source.commands.commands_executor.commands_executor_mvc.commands_executor_model import CommandsExecutorModel
from source.commands.commands_executor.commands_executor_mvc.commands_executor_view import CommandsExecutorView
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.shortcats.shortcat_getter import ShortcatGetter
from source.shortcats.shortcat_listener import ShortcatListener



class CommandsExecutorController(QObject):
    #listener надо будет отключать при записи других клавиш, поэтому, подключим сигналы.
    # А также не будем давать возможность 
    start_executing_signal = Signal()
    stop_executing_signal = Signal()
    resume_executing_signal = Signal()
    params_updated_signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = CommandsExecutorView()
        self.model = CommandsExecutorModel()
        

        self._shortcats_getters = [
            self.view.shortcat_start_getter,
            self.view.shortcat_resume_getter,
            self.view.shortcat_stop_getter
        ]
        for i, shortcat_getter in enumerate(self._shortcats_getters):
            shortcat_getter.combination_recording_started_signal.connect(lambda j=i: self._shortcat_started_listening_slot(self._shortcats_getters[j]))
            shortcat_getter.combination_recording_done_signal.connect(lambda j=i: self._some_shortcat_updated(self._shortcats_getters[j]))        
        
        self.shortcats_listener = ShortcatListener(on_keys_updated=self._keys_listener_commands)
        self.shortcats_listener.start()
        self.view.params_changed_signal.connect(self._params_changed)

    def _some_shortcat_updated(self, getter:ShortcatGetter):
        flag = True
        for item in self._shortcats_getters:
            if(item.is_recording()):
                flag = False
                break

        if(flag):
            self.shortcats_listener.start()

    def _shortcat_started_listening_slot(self, getter:ShortcatGetter):
        self.shortcats_listener.stop()
        for item in self._shortcats_getters:
            if(item!=getter):
                item.cancel_recording()
    
    def _keys_listener_commands(self, keys):
        matched_getter = None
        for getter in self._shortcats_getters:
            if(ShortcatMatcher.match(expected=getter.keys, current=keys)):
                matched_getter = getter
                break
        if(matched_getter):

            if(matched_getter==self.view.shortcat_start_getter):
                self.start_executing_signal.emit()
            elif(matched_getter==self.view.shortcat_resume_getter):
                # 
                self.resume_executing_signal.emit()
            elif(matched_getter==self.view.shortcat_stop_getter):
                
                self.stop_executing_signal.emit()
            
            print(matched_getter, matched_getter.keys)

    def get_executing_time_ms(self):
        return self.view.deltatime_spinbox.value()/1000.0
    def _params_changed(self):
        '''view params can be changed, handling is here'''
        self.params_updated_signal.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    

    
    ex = CommandsExecutorController()


    commands_iterator = CommandsIterator([
        MoveMouseGlobal(10,10),
        MoveMouseGlobal(100,100),
        MoveMouseGlobal(400,400),
        MoveMouseGlobal(800,800),
        MoveMouseGlobal(200,200),
        MoveMouseGlobal(150,150),
        MoveMouseGlobal(10,10),
        MoveMouseGlobal(100,100),
        MoveMouseGlobal(400,400),
        MoveMouseGlobal(800,800),
        MoveMouseGlobal(200,200),
        MoveMouseGlobal(150,150),
    ]
                                         , width=400, height=400)
    
    
    commands_executor_thread = CommandsExecutorThread()
    commands_executor_thread.start()
    commands_executor_thread.set_commands_iterator(commands_iterator=commands_iterator)

    def commands_executor_thread_start_signal():
        commands_executor_thread.set_commands_iterator(commands_iterator)
        commands_executor_thread.restart_iterations()
    def commands_executor_thread_resume_signal():
        commands_executor_thread.resume_iterations()
    def commands_executor_thread_stop_signal():
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