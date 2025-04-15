import numpy as np
from skimage.transform import resize

class Utils:
    @staticmethod


    def resize_array(array: np.ndarray, new_width: int, new_height: int) -> np.ndarray:
        """
        Универсальное масштабирование NumPy массива с билинейной интерполяцией.
        Поддержка grayscale, RGB, RGBA, ARGB и binary.

        :param array: NumPy массив изображения (H, W), (H, W, 3), (H, W, 4)
        :param new_width: Новая ширина
        :param new_height: Новая высота
        :return: Масштабированный NumPy массив
        """
        src_height, src_width = array.shape[:2]
        is_binary = array.dtype == np.bool_ or np.array_equal(np.unique(array), [0, 1])

        # Преобразование в float32 для безопасной интерполяции
        arr = array.astype(np.float32)
        if arr.ndim == 2:
            arr = arr[:, :, np.newaxis]  # преобразуем grayscale в (H, W, 1)

        channels = arr.shape[2]

        # Создаём координатную сетку выходного изображения
        y = np.linspace(0, src_height - 1, new_height)
        x = np.linspace(0, src_width - 1, new_width)
        x_grid, y_grid = np.meshgrid(x, y)

        x0 = np.floor(x_grid).astype(int)
        x1 = np.clip(x0 + 1, 0, src_width - 1)
        y0 = np.floor(y_grid).astype(int)
        y1 = np.clip(y0 + 1, 0, src_height - 1)

        x_weight = x_grid - x0
        y_weight = y_grid - y0

        result = np.zeros((new_height, new_width, channels), dtype=np.float32)

        for c in range(channels):
            a = arr[y0, x0, c]
            b = arr[y0, x1, c]
            c_ = arr[y1, x0, c]
            d = arr[y1, x1, c]

            top = a * (1 - x_weight) + b * x_weight
            bottom = c_ * (1 - x_weight) + d * x_weight
            result[:, :, c] = top * (1 - y_weight) + bottom * y_weight

        # Возвращаем нужный формат
        result = np.clip(result, 0, 1 if is_binary else 255)

        if is_binary:
            result = (result > 0.5).astype(np.uint8)
        else:
            result = result.astype(array.dtype)

        if result.shape[2] == 1:
            result = result[:, :, 0]  # возвращаем обратно 2D

        return result

    @staticmethod
    def generate_numpy_canvas(shape):
        return np.zeros(shape=shape)
