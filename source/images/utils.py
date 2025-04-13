import numpy as np

class Utils:
    @staticmethod
    def resize_array(array: np.ndarray, new_width: int, new_height: int) -> np.ndarray:
        """
        Ручное сжатие/масштабирование NumPy массива с билинейной интерполяцией.
        
        :param image: NumPy-массив (H, W) или (H, W, C)
        :param new_width: новая ширина
        :param new_height: новая высота
        :return: масштабированное изображение
        """
        src_height, src_width = array.shape[:2]
        channels = 1 if array.ndim == 2 else array.shape[2]
        
        # Подготовка выходного массива
        if channels == 1:
            resized = np.zeros((new_height, new_width), dtype=array.dtype)
        else:
            resized = np.zeros((new_height, new_width, channels), dtype=array.dtype)
        
        # Соотношение размеров
        x_ratio = src_width / new_width
        y_ratio = src_height / new_height
        
        for y in range(new_height):
            for x in range(new_width):
                # координаты в оригинальном изображении
                x_l = int(np.floor(x * x_ratio))
                y_l = int(np.floor(y * y_ratio))
                x_h = min(x_l + 1, src_width - 1)
                y_h = min(y_l + 1, src_height - 1)
                
                x_weight = (x * x_ratio) - x_l
                y_weight = (y * y_ratio) - y_l
                
                if channels == 1:
                    a = array[y_l, x_l]
                    b = array[y_l, x_h]
                    c = array[y_h, x_l]
                    d = array[y_h, x_h]
                    
                    top = a * (1 - x_weight) + b * x_weight
                    bottom = c * (1 - x_weight) + d * x_weight
                    value = top * (1 - y_weight) + bottom * y_weight
                    resized[y, x] = np.clip(value, 0, 255)
                else:
                    for c in range(channels):
                        a = array[y_l, x_l, c]
                        b = array[y_l, x_h, c]
                        c_ = array[y_h, x_l, c]
                        d = array[y_h, x_h, c]
                        
                        top = a * (1 - x_weight) + b * x_weight
                        bottom = c_ * (1 - x_weight) + d * x_weight
                        value = top * (1 - y_weight) + bottom * y_weight
                        resized[y, x, c] = np.clip(value, 0, 255)

        return resized.astype(array.dtype)
    @staticmethod
    def generate_numpy_canvas(shape):
        return np.zeros(shape=shape)
