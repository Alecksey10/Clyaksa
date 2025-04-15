import pathlib
import sys
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

import numpy as np

sys.path.append('.')


from source.images.color_schemas import ColorSchemas
from source.images.image_objects_data_extractor import ImageObjectsDataExtractor

from source.images.image_object_binary import ImageObjectBinary
from source.images.image_object_ARGB import ImageObjectARGB
from source.images.image_object_base import ImageObjectBase


class ImageObjectsFabric():
    
    @staticmethod
    def rgba_from_numpy(arr:np.ndarray)->ImageObjectARGB:
        if(len(arr.shape)!=3):
            raise Exception(f"incorrect arr shape {arr.shape}")
        if(arr.shape[2]!=4):
            raise Exception(f"incorrect arr depth {arr.shape}")
        return ImageObjectARGB(arr.copy())
    
    @staticmethod
    def binary_from_numpy(arr:np.ndarray)->ImageObjectBinary:
        if(len(arr.shape)!=2):
            raise Exception(f"incorrect arr shape {arr.shape}")
        return ImageObjectBinary(arr.copy())
    
    @staticmethod
    def from_numpy_and_color_schemas(arr:np.ndarray, color_schemas:ColorSchemas)->ImageObjectBinary:
        if(color_schemas==ColorSchemas.ARGB):
            return ImageObjectsFabric.rgba_from_numpy(arr)
        elif(color_schemas==ColorSchemas.Binary):
            return ImageObjectsFabric.binary_from_numpy(arr)
        else:
            raise Exception("there is no such color_schemas")
    
    @staticmethod
    def from_any_to_color_schema(image:ImageObjectBase, result_color_scheme:ColorSchemas)->ImageObjectBase:
        current_color_scheme = image.get_color_scheme()

        if(current_color_scheme==result_color_scheme):
            #просто копируем в новый объект
            return ImageObjectsFabric.from_numpy_and_color_schemas(image.get_as_numpy(), color_schemas=result_color_scheme)

        if(result_color_scheme==ColorSchemas.ARGB):
            if(current_color_scheme==ColorSchemas.Binary):
                image:ImageObjectBase
                data:np.ndarray = image.get_as_numpy()
                color_image = np.repeat(data[:, :, np.newaxis], 4, axis=2)
                return ImageObjectsFabric.rgba_from_numpy(color_image)
            else:
                raise Exception(f"there is no such color_schema {result_color_scheme} {current_color_scheme}")
        elif(result_color_scheme==ColorSchemas.Binary):
            if(current_color_scheme==ColorSchemas.ARGB):
                data:np.ndarray = image.get_as_numpy()
                binary_image = 0.299 * data[:,:,0] + 0.587 * data[:,:,1] + 0.114 * data[:,:,2]
                return ImageObjectsFabric.binary_from_numpy(binary_image.astype(np.uint8))
        else:
            raise Exception("there is no such color_schemas")
    

    @staticmethod
    def empty_rgba()->ImageObjectARGB:
        arr = np.zeros(shape=(10,10,4))
        return ImageObjectARGB(arr.copy())
def main():
    pass

if __name__=="__main__":
    from source.images.image_object_widget import ImageObjectWidget
    from source.images.image_objects_visualizer import ImageObjectsVisualizer
    
    path = pathlib.Path("./assets/fly.jpg")
    img = QImage()
    print(path.absolute())
    img.load(str(path.absolute()))
    data = ImageObjectsDataExtractor.qimage_to_numpy(image=img)
    print(data.shape)
    img_obj = ImageObjectsFabric.rgba_from_numpy(data)
    img_obj = ImageObjectsFabric.from_any_to_color_schema(img_obj, result_color_scheme=ColorSchemas.Binary)
    print(img_obj, img_obj.data.shape, img_obj.get_color_scheme(), img_obj.width)

    qimage2 = ImageObjectsVisualizer.convert_image_obj_to_qimage(img_obj)


    app = QApplication(sys.argv)

    label = ImageObjectWidget()
    label.set_image(img)
    label.show()

    
    label2 = ImageObjectWidget()
    label2.set_image(qimage2)
    label2.show()

    sys.exit(app.exec())

