

import copy
from dataclasses import dataclass

import math
import sys
sys.path.append(".")
from source.commands.command_base import CommandBase
from source.commands.move_mouse_global import MoveMouseGlobal

@dataclass
class CommandsTransformator:
    '''почти полностью написан нейронкой, лучше не доделывать, а переписать с нуля. '''
    #TODO это трансформатор команд или всё таки точек каких-нибудь? также слабоват трансформатор что-то...
    rotation_deg: float = 0.0
    scale: float = 1.0
    shift_x: float = 0.0
    shift_y: float = 0.0

    rotation_center_x: float = 0.0  # Центр трансформации по X
    rotation_center_y: float = 0.0  # Центр трансформации по Y

    scale_center_x: float = 0.0  # Центр трансформации по X
    scale_center_y: float = 0.0  # Центр трансформации по Y

    tolerance_rotation: float = 1e-2
    tolerance_scale: float = 1e-2
    tolerance_shift: float = 1e-2

    def apply_to_point(self, x: float, y: float) -> tuple[float, float]:
        """
        Применяет трансформацию к точке (x, y):
        1. Масштабирование относительно scale-центра
        2. Поворот относительно rotation-центра
        3. Сдвиг
        """

        # --- Масштаб относительно scale центра ---
        x_scaled = (x - self.scale_center_x) * self.scale + self.scale_center_x
        y_scaled = (y - self.scale_center_y) * self.scale + self.scale_center_y

        # --- Поворот относительно rotation центра ---
        dx = x_scaled - self.rotation_center_x
        dy = y_scaled - self.rotation_center_y

        rad = math.radians(self.rotation_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        x_rot = dx * cos_a - dy * sin_a + self.rotation_center_x
        y_rot = dx * sin_a + dy * cos_a + self.rotation_center_y

        # --- Финальный сдвиг ---
        x_final = x_rot + self.shift_x
        y_final = y_rot + self.shift_y

        return x_final, y_final
    
    def apply_transform_to_command(self, command:CommandBase) -> None:
        if(isinstance(command,MoveMouseGlobal)):
            current_pos = self.apply_to_point(command.x, command.y)
            command.x = current_pos[0]
            command.y = current_pos[1]


    def transform_command(self, command:CommandBase) -> CommandBase:
        new_command = copy.copy(command)
        self.apply_transform_to_command(new_command)
        return new_command

transformator = CommandsTransformator()
transformator.shift_x = 0
transformator.shift_y = 0
transformator.rotation_center_x = 3
transformator.rotation_center_y = -2
transformator.scale_center_x = 3
transformator.scale_center_y = -2
transformator.rotation_deg = 90
transformator.scale = 2

print(transformator.apply_to_point(4, -2)) # -4, -2 > 3.0, 0

transformator = CommandsTransformator()
transformator.shift_x = 3
transformator.shift_y = -2
transformator.rotation_center_x = 0
transformator.rotation_center_y = 0
transformator.scale_center_x = 0
transformator.scale_center_y = 0
transformator.rotation_deg = 90
transformator.scale = 2

print(transformator.apply_to_point(1, 0)) # -4, -2 > 3.0, 0
print(transformator.apply_to_point(2, 0)) # -4, -2 > 3.0, 2

# transformator = CommandsTransformator()
# transformator.shift_x = 0
# transformator.shift_y = 0
# transformator.rotation_center_x = 20
# transformator.rotation_center_y = 20
# transformator.scale_center_x = 20
# transformator.scale_center_y = 20
# transformator.rotation_deg = 90
# transformator.scale = 2

# print(transformator.apply_to_point(10, 10)) # -4, -2 > 3.0, 0