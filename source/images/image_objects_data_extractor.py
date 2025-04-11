from PySide6.QtGui import QImage
import numpy as np
import pathlib

class ImageObjectsDataExtractor():
    
    @staticmethod
    def qimage_to_numpy(image: QImage) -> np.ndarray:
        image = image.convertToFormat(QImage.Format.Format_RGBA8888)
        width = image.width()
        height = image.height()

        # Получаем memoryview напрямую
        ptr = image.bits()
        buffer = memoryview(ptr)  # memoryview уже правильного размера

        arr = np.asarray(buffer).reshape((height, width, 4))
        return arr.copy()  # <- копия на случай, если QImage будет уничтожен
    

def main():
    pass

if __name__=="__main__":
    path = pathlib.Path("./assets/fly.jpg")
    img = QImage()
    print(path.absolute())
    img.load(str(path.absolute()))

    data = ImageObjectsDataExtractor.qimage_to_numpy(image=img)
    print(data.shape)