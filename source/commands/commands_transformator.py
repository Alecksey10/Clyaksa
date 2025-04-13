

from dataclasses import dataclass

import math

@dataclass
class CommandsTransformator:
    rotation_deg: float = 0.0
    scale: float = 1.0
    shift_x: float = 0.0
    shift_y: float = 0.0

    rotation_center_x: float = 0.0  # Центр трансформации по X
    rotation_center_y: float = 0.0  # Центр трансформации по Y

    tolerance_rotation: float = 1e-2
    tolerance_scale: float = 1e-2
    tolerance_shift: float = 1e-2

    def apply_to_point(self, x: float, y: float) -> tuple[float, float]:
        """
        Применяет трансформацию к точке (x, y) с учётом центра трансформации.
        Последовательность: перенос → масштабирование и поворот → обратный перенос → сдвиг.
        """
        # Переносим точку в систему координат с центром в (center_x, center_y)
        x =x*self.scale- self.rotation_center_x
        y =y*self.scale- self.rotation_center_y

        # Масштабирование
        # x *= self.scale
        # y *= self.scale

        # Поворот
        rad = math.radians(self.rotation_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        x_rot = x * cos_a - y * sin_a
        y_rot = x * sin_a + y * cos_a

        # Переносим обратно и применяем сдвиг
        x_final = x_rot + self.rotation_center_x + self.shift_x
        y_final = y_rot + self.rotation_center_y + self.shift_y

        # x_final *= self.scale
        # y_final*= self.scale

        return x_final, y_final