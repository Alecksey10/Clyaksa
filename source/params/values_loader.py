import pathlib
import json

import sys
sys.path.append(".")
from source.params.params_scheme_base import ParamsSchemeBase
from source.params.params_scheme_json import ParamsSchemeJson
from source.params.stricts_loader import StrictsLoader

class ValuesLoader():

    @staticmethod
    def load_values_from_json(path: pathlib.Path, params_scheme_base: ParamsSchemeBase):
        obj:dict = None
        with open(path.absolute(), mode="r", encoding="utf-8") as file:
            obj = json.load(file)
        
        for key, value in obj.items():
            if not params_scheme_base.try_set_param_by_name(name=key, value=value):
                raise Exception(f"cannot load values to scheme from path, path:{path.absolute()}, key:{key}, value:{value}")    
    @staticmethod
    def load_values_scheme_from_pydantic(cls:type) -> ParamsSchemeJson:
        ...



        
def main():
    p:ParamsSchemeBase = StrictsLoader.load_fields_scheme_from_json(pathlib.Path("./assets/stricts.json"))
    print(p.get_params_obj())
    print(p.get_params_as_dict())
    ValuesLoader.load_values_from_json(pathlib.Path("./assets/values.json"), p)
    print(p.get_params_obj())
    print(p.get_param_by_name("B"))
    print(p.get_params_as_dict())

if __name__=="__main__":
    main()