from threading import Lock, Thread
import time

from source.commands.commands_executor.commands_executor import CommandsExecutor
from source.commands.commands_iterator.commands_iterator import CommandsIterator

class CommandsExecutorThread(Thread):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b_is_running = False
        self.b_need_stop = False
        self.b_need_terminate = False
        self.b_is_done = False
        self.running_lock = Lock()

        self.commands_iterator = CommandsIterator([])
        self.commands_executor = CommandsExecutor()
        self.delta_time:float = 0.04

    def run(self):
        self.b_is_running = True
        self.b_need_stop = False
        while not self.b_need_terminate:
            
            if(not self.b_is_running):
                time.sleep(0.01)
                continue
            try:
                self.running_lock.acquire()
                next_command = next(self.commands_iterator)
                self.commands_executor.execute_command(next_command)
                
            except StopIteration:
                self.stop_iterations()
                self.b_is_done = True
            except Exception as ex:
                self.stop_iterations()
                self.b_is_done = True
                raise ex
            finally:
                self.running_lock.release()
                time.sleep(self.delta_time)


    
    def set_commands_iterator(self, commands_iterator:CommandsIterator):
        self.running_lock.acquire()
        self.commands_iterator = commands_iterator
        self.commands_iterator.restart()
        self.running_lock.release()

    def set_delta_time(self, delta_time:float):
        self.delta_time = delta_time
        
    

    def stop_thread(self):
        self.b_need_terminate = True
        pass

    def restart_iterations(self):
        self.running_lock.acquire()
        self.commands_iterator.restart()
        self.b_is_running = True
        self.running_lock.release()
        pass

    def resume_iterations(self):
        self.b_is_running = True
        pass
    
    def stop_iterations(self):
        self.b_is_running = False
        pass
