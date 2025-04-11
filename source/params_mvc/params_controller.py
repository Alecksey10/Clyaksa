import pathlib
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QApplication, QComboBox
)
from PySide6.QtCore import QObject, Signal
import sys
sys.path.append('.')

from source.params.fields.combobox_field import ComboboxField
from source.params_mvc.params_view import ParamsView

from source.params.fields.float_field import FloatField
from source.params.fields.int_field import IntField
from source.params.stricts_loader import StrictsLoader
from source.params.values_loader import ValuesLoader
from source.params.params_scheme_base import ParamsSchemeBase


class ParamsController(QObject):
    # Сигнал, который отправляет (имя_поля, новое_значение)
    params_updated_signal = Signal(object)
    # params_applied_signal = Signal(str, object)

    def __init__(self, config: ParamsSchemeBase):
        super().__init__()
        self.params_scheme:ParamsSchemeBase = config
        self.widgets = {}
        self.view = self._build_view()

        self.view.params_updated_signal.connect(self.params_updated_slot)

    def _build_view(self) -> ParamsView:
        widget = ParamsView()
        layout = QFormLayout(widget)
        params_dict = self.params_scheme.get_params_as_dict()
        for field in self.params_scheme.fields:
            name = field.name
            # display_type = field ["display_type"]
            if isinstance(field,IntField):
                spin = QSpinBox()
                spin.setRange(getattr(field , "min", -99999), getattr(field , "max", 99999))
                spin.setSingleStep(getattr(field , "step", 1))
                spin.setValue(params_dict[name])
                spin.valueChanged.connect(lambda val, name=name: widget.params_updated_signal.emit(name, val))
                layout.addRow(name, spin)
                self.widgets[name] = spin

            elif isinstance(field,FloatField):
                spin = QDoubleSpinBox()
                spin.setRange(getattr(field , "min", -1e10), getattr(field , "max", 1e10))
                spin.setSingleStep(getattr(field , "step", 0.1))
                spin.setDecimals(6)
                spin.setValue(params_dict[name])
                spin.valueChanged.connect(lambda val, name=name: widget.params_updated_signal.emit(name, val))
                layout.addRow(name, spin)
                self.widgets[name] = spin

            
            elif isinstance(field,ComboboxField):
                combobox = QComboBox()
                values = getattr(field , "values", ["None"])
                for value in values:
                    combobox.addItem(value)
                
                for i, value in enumerate(values):
                    if(combobox.itemText(i)==params_dict[name]):
                        combobox.setCurrentIndex(i)
                        break
                
                combobox.currentTextChanged.connect(lambda val, name=name: widget.params_updated_signal.emit(name, val))
                layout.addRow(name, combobox)
                self.widgets[name] = combobox

            else:
                print(f"⚠️ Unsupported type or display_type for {name}")
        return widget

    def params_updated_slot(self, name, val, *args, **kwargs):
        res = self.params_scheme.try_set_param_by_name(name=name, value=val)
        self.params_updated_signal.emit(self.params_scheme)
        pass
    
    def get_view(self) -> QWidget:
        return self.view

    def set_value(self, name: str, value):
        """Обновить значение поля программно (без сигнала)"""
        widget = self.widgets.get(name)
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.blockSignals(True)
            widget.setValue(value)
            widget.blockSignals(False)

    def get_value(self, name: str):
        widget = self.widgets.get(name)
        return widget.value() if widget else None
    


def main():
    app = QApplication(sys.argv)

    p:ParamsSchemeBase = StrictsLoader.load_fields_scheme_from_json(pathlib.Path("./assets/stricts.json"))
    ValuesLoader.load_values_from_json(pathlib.Path("./assets/values.json"), p)

    controller = ParamsController(p)

    view = controller.get_view()
    view.show()

    def handle_change(config:ParamsSchemeBase):
        print(config.get_params_as_dict())

    controller.params_updated_signal.connect(handle_change)

    sys.exit(app.exec())


if __name__=="__main__":
    main()