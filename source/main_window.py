import pathlib
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QHBoxLayout, QPushButton,QFileDialog, QMenuBar, QMenu
)

from PySide6.QtGui import QAction, QImage
from PySide6.QtCore import Qt
import sys

sys.path.append(".")
from source.commands.commands_executor.commands_executor_thread import CommandsExecutorThread

from source.commands.commands_executor.commands_executor_mvc.commands_executor_controller import CommandsExecutorController
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.commands.commands_vizualizer.commands_vizualizer_controller import CommandsVizualizerController
from source.widgets.image_visualizer import ImageVizualizer

from source.commands.commands_generator_mvc.commands_generator_controller_base import CommandsGeneratorControllerBase
from source.images.image_objects_visualizer import ImageObjectsVisualizer

from source.image_filters_algorithms.image_destructurizator_mvc.image_destructurizator_controller import ImageDestructurizatorController
from source.images.image_object_base import ImageObjectBase
from source.images.image_object_widget import ImageObjectWidget
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor
from source.images.image_objets_fabric import ImageObjectsFabric


class MainWindow(QMainWindow):
    def __init__(self):
        self.original_image_object:ImageObjectBase = ImageObjectsFabric.empty_rgba()
        self.filtered_image_object: ImageObjectBase = ImageObjectsFabric.empty_rgba()
        self.pinned_image_object: ImageObjectBase = ImageObjectsFabric.empty_rgba()
        

        self.original_image_widget:ImageObjectWidget = ImageObjectWidget()
        self.original_image_widget.setWindowTitle("Оригинальное изображение")
        self.filtered_image_widget:ImageObjectWidget = ImageObjectWidget()
        self.filtered_image_widget.setWindowTitle("Фильтрованное изображение")
        self.current_commands_iterator = CommandsIterator([])


        super().__init__()
        self._build_ui()
    
    def _build_ui(self):
        self.setWindowTitle("Жирный MainWindow со стрелками")
        self.setMinimumSize(800, 600)


        self.build_tab_widget()
        self.build_menu_bar()

        #Соберём по кусочкам gui, 
        # 1) для фильтрации изображений
        self.image_destructurizator_controller = ImageDestructurizatorController(self.original_image_object.width,
                                                                                  self.original_image_object.height)
        self.image_destructurizator_controller.view.show()
        self.image_destructurizator_controller.apply_filter_signal.connect(self.apply_filter_slot)
        self.image_destructurizator_controller.apply_filter_to_pinned_signal.connect(self.apply_filter_to_pinned_slot)
        self.image_destructurizator_controller.pinn_filtered_image_signal.connect(self.pinn_filtered_image_slot)


        self.tab1_layout.addWidget(self.image_destructurizator_controller.view)

        # 2.A) для генерации команд
        self.commands_generator_controller_base = CommandsGeneratorControllerBase()
        self.commands_generator_controller_base.view.show()
        self.commands_generator_controller_base.generate_btn_pressed_signal.connect(self.generator_btn_handler)

        self.tab2_layout.addWidget(self.commands_generator_controller_base.view)
        

        # 2.B) по идее параллельно (логически) также надо собрать логику для визуализации команд и настройки визуализации
        self.commands_vizualizer_controller = CommandsVizualizerController()
        self.commands_vizualizer_controller.view.setWindowTitle("Контролы")
        self.commands_vizualizer_controller.view.resize(300, 300)
        self.commands_vizualizer_controller.view.show()
        self.commands_vizualizer_controller.params_updated_signal.connect(self.vizualization_controller_params_update_slot)
        
        self.tab3_layout.addWidget(self.commands_vizualizer_controller.view)

        # 2.C) и окно для самой визуализации команд
        self.vizualizated_commands_window = ImageVizualizer()
        self.vizualizated_commands_window.drag_and_drop  = True
        self.vizualizated_commands_window.click_through = False
        # self.vizualizated_commands_window.always_on_top = False
        self.vizualizated_commands_window.opacity = 0.4
        self.vizualizated_commands_window.position_changed_signal.connect(self.vizualizate_window_movement_slot)
        
        self.vizualizated_commands_window.show()

        #Теперь подключаем исполнитель команд
        self.commands_executor_controller = CommandsExecutorController()    
        
        self.commands_executor_thread = CommandsExecutorThread()
        self.commands_executor_thread.start()
        self.commands_executor_thread.set_commands_iterator(commands_iterator=self.current_commands_iterator)
        self.commands_executor_thread.iterations_done_signal.connect(self.commands_executor_thread_is_done_slot)

        self.tab4_layout.addWidget(self.commands_executor_controller.view)

        self.commands_executor_controller.start_executing_signal.connect(self.commands_executor_thread_start_slot)
        self.commands_executor_controller.resume_executing_signal.connect(self.commands_executor_thread_resume_slot)
        self.commands_executor_controller.stop_executing_signal.connect(self.commands_executor_thread_stop_slot)
        self.commands_executor_controller.params_updated_signal.connect(self.commands_executor_thread_params_changed)


        self._on_tab_changed(0)
        

    def build_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = QMenu("Файл", self)
        menu_bar.addMenu(file_menu)
        
        # --- Действие: Открыть файл ---
        open_action = QAction("Открыть изображение...", self)
        open_action.triggered.connect(self._open_file_dialog)
        file_menu.addAction(open_action)

        # --- Действие: Выход ---
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(app.exit)
        file_menu.addAction(exit_action)
        
    def build_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # --- Вкладка 1 ---
        self.tab1 = self._create_tab_with_arrows()
        self.tab1_layout = self.tab1.layout().itemAt(0).layout()

        # self.tab1_main = QLabel("Основной виджет вкладки 1")
        # self.tab1_extra1 = QLabel("Дополнительный виджет 1 (tab1)")
        # self.tab1_extra2 = QLabel("Дополнительный виджет 2 (tab1)")

        # self.tab1_extra1.hide()
        # self.tab1_extra2.hide()

        # self.tab1_layout.addWidget(self.tab1_main)
        # self.tab1_layout.addWidget(self.tab1_extra1)
        # self.tab1_layout.addWidget(self.tab1_extra2)

        # --- Вкладки 2–4 ---
        self.tab2 = self._create_tab_with_arrows()
        self.tab2_layout = self.tab2.layout().itemAt(0).layout()

        self.tab3 = self._create_tab_with_arrows()
        self.tab3_layout = self.tab3.layout().itemAt(0).layout()

        self.tab4 = self._create_tab_with_arrows()
        self.tab4_layout = self.tab4.layout().itemAt(0).layout()

        self.tab_widget.addTab(self.tab1, "Вкладка 1")
        self.tab_widget.addTab(self.tab2, "Вкладка 2")
        self.tab_widget.addTab(self.tab3, "Вкладка 3")
        self.tab_widget.addTab(self.tab4, "Вкладка 4")

        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self._on_tab_changed(0)

    def _create_tab_with_arrows(self) -> QWidget:
        tab = QWidget()
        outer_layout = QVBoxLayout(tab)
        content_layout = QVBoxLayout()
        arrow_layout = QHBoxLayout()

        btn_prev = QPushButton("←")
        btn_next = QPushButton("→")

        btn_prev.clicked.connect(self._go_to_prev_tab)
        btn_next.clicked.connect(self._go_to_next_tab)

        arrow_layout.addStretch()
        arrow_layout.addWidget(btn_prev)
        arrow_layout.addWidget(btn_next)
        arrow_layout.addStretch()

        outer_layout.addLayout(content_layout)  # верхний layout для пользовательских виджетов
        outer_layout.addLayout(arrow_layout)    # нижняя панель со стрелками

        return tab

    def _on_tab_changed(self, index: int):
        print(f"tab changed {index}")
        if index == 0:
            self.original_image_widget.show()
            self.filtered_image_widget.show()
            self.raise_()
        else:
            self.original_image_widget.hide()
            self.filtered_image_widget.hide()


    def set_tab_widget_by_index(self, index):
        
        self.tab_widget.setCurrentIndex(index)

    def _go_to_prev_tab(self):
        index = self.tab_widget.currentIndex()
        if index > 0:
            self.set_tab_widget_by_index(index-1)

    def _go_to_next_tab(self):
        index = self.tab_widget.currentIndex()
        if index < self.tab_widget.count() - 1:
            self.set_tab_widget_by_index(index+1)

    def get_tab_layout(self, tab_index: int) -> QVBoxLayout:
        return getattr(self, f"tab{tab_index+1}_layout", None)

    def _open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл")
        if path:
            path = pathlib.Path(path)
            qimage1 = QImage()
            qimage1.load(str(path.absolute()))
            qimage1.convertTo(QImage.Format.Format_ARGB32)
            print(qimage1.size(),"width",qimage1.width(), qimage1)
            # преобразуем в numpy
            data = ImageObjectsDataExtractor.qimage_to_numpy(image=qimage1)
            print(data.shape)
            # Преобразуем к нашему формату ImageObjectBase
            self.original_image_object = ImageObjectsFabric.rgba_from_numpy(data)

            self.original_image_widget.set_image(qimage1)
            self.original_image_widget.resize_to_content()
            self.filtered_image_widget.set_image(qimage1)
            self.filtered_image_widget.resize_to_content()

            self.image_destructurizator_controller.update_settings_to_image_size(qimage1.width(), qimage1.height())


    def apply_filter_slot(self):
        self.filtered_image_object = self.image_destructurizator_controller.apply_algorithm_to_image(self.original_image_object)
        self.filtered_image_widget.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(self.filtered_image_object))
        pass

    def apply_filter_to_pinned_slot(self):
        self.filtered_image_object = self.image_destructurizator_controller.apply_algorithm_to_image(self.pinned_image_object)
        self.filtered_image_widget.set_image(ImageObjectsVisualizer.convert_image_obj_to_qimage(self.filtered_image_object))
        pass

    def pinn_filtered_image_slot(self):
        self.pinned_image_object = self.filtered_image_object
        pass
    
    def vizualization_controller_params_update_slot(self):
        self.vizualizate_commands(self.current_commands_iterator)

    def vizualizate_window_movement_slot(self):
        pos = self.vizualizated_commands_window.get_internal_pos()
        self.commands_vizualizer_controller.update_transform_shift(pos.x(), pos.y())

    def vizualizate_commands(self,commands_iterator):
        if (commands_iterator == None):
            return
        self.commands_vizualizer_controller.set_commands_iterator(commands_iterator)
        vizualizated_commands_qimage = self.commands_vizualizer_controller.get_commands_visualization()
        self.vizualizated_commands_window.set_image(vizualizated_commands_qimage)
        pass

    def generator_btn_handler(self):
        if(not self.filtered_image_object):
            return
        self.commands_generator_controller_base.process_image(self.filtered_image_object)
        self.current_commands_iterator = self.commands_generator_controller_base.get_commands_iterator()
        print(self.current_commands_iterator, "количество комманд:", len(self.current_commands_iterator))
        self.vizualizate_commands(self.current_commands_iterator)

    def commands_executor_thread_start_slot(self):
        
        #иначе ранее зажатые горячие клавиши могут пересечься с ненужным фукнкционалом. И мышь будет кликаться с одной из зажатых клавишей
        time.sleep(1)
        self.vizualizated_commands_window.hide()
        transformed_commands = []
        self.current_commands_iterator.restart()
        for command in self.current_commands_iterator:
            transformed_commands.append(self.commands_vizualizer_controller.commands_transformator.transform_command(command=command))

        transformed_commands_iterator = CommandsIterator(transformed_commands, width = self.current_commands_iterator.width, height = self.current_commands_iterator.height)

        self.commands_executor_thread.set_commands_iterator(transformed_commands_iterator)


        self.commands_executor_thread.restart_iterations()
    def commands_executor_thread_resume_slot(self):
        time.sleep(1)
        self.vizualizated_commands_window.hide()
        self.commands_executor_thread.resume_iterations()
    def commands_executor_thread_stop_slot(self):
        self.vizualizated_commands_window.show()
        self.commands_executor_thread.stop_iterations()

    def commands_executor_thread_params_changed(self):
        print(self.commands_executor_controller.get_executing_time_ms())
        self.commands_executor_thread.set_delta_time(self.commands_executor_controller.get_executing_time_ms())
    
    def commands_executor_thread_is_done_slot(self):
        self.vizualizated_commands_window.show()  

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()