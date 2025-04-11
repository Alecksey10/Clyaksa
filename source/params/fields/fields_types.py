from enum import Enum


class FieldsTypes(Enum):
    Int = 0
    Float = 1
    Combobox = 2
    Bool = 3


if __name__=="__main__":
    assert ((0) in FieldsTypes)
    assert ("Int"==FieldsTypes.Int.name)