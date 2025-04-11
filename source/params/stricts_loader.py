import pathlib
import json
import sys

sys.path.append(".")
from source.params.fields.fields_types import FieldsTypes
from source.params.fields.display_types import DisplayTypes
from source.params.fields.field import FieldStricts
from source.params.fields import int_field, float_field, bool_field, combobox_field
from source.params.params_scheme_json import ParamsSchemeJson
class StrictsLoader():
    @staticmethod
    def load_fields_scheme_from_json(path: pathlib.Path) -> ParamsSchemeJson:
        obj:dict = None
        with open(path.absolute(), mode="r", encoding="utf-8") as file:
            obj = json.load(file)
        
        # SOLID, open close нарушаю как минимум
        fields = []
        for key, item in obj.items():
            field_params = {}
            # Для json всё тривиально
            field_params = item
            # Фабрика нужна
            if(item["type"]==FieldsTypes.Int.name):
                fields.append(int_field.IntField(strcits_dict=field_params))
            if(item["type"]==FieldsTypes.Float.name):
                fields.append(float_field.FloatField(strcits_dict=field_params))
            if(item["type"]==FieldsTypes.Bool.name):
                fields.append(bool_field.BoolField(strcits_dict=field_params))
            if(item["type"]==FieldsTypes.Combobox.name):
                fields.append(combobox_field.ComboboxField(strcits_dict=field_params))
        
        return ParamsSchemeJson(fields=fields)
    
    @staticmethod
    def load_fields_scheme_from_pydantic(cls:type) -> ParamsSchemeJson:
        ...
    

        

def main():
    p = StrictsLoader.load_fields_scheme_from_json(pathlib.Path("./assets/stricts.json"))
    print(p)
    print(p.get_params_as_dict())

if __name__=="__main__":
    main()
        
