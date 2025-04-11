
from typing import List
from source.params.params_obj import ParamsObj
import abc
from source.params.fields.field import FieldStricts

class ParamsSchemeBase(abc.ABC):

    @abc.abstractmethod
    def __init__(self, fields:List[FieldStricts]):
        self._params_obj:ParamsObj = None
        self.fields:List[FieldStricts] = []

    def get_params_obj(self):
        return self._params_obj

    @abc.abstractmethod
    def get_param_by_name(self, name:str):
        pass

    def get_params_as_dict(self):
        result = {}
        for field in self.fields:
            result[field.name]=self.get_param_by_name(field.name)
        return result


    def try_set_param_by_name(self, name:str, value, *args, **kwargs) -> bool:
        #Мб переделать на dict?, не очень перебор..
        result_flag = False
        for field in self.fields:
            if(field.name==name):
                if(field.validate(value)):
                    setattr(self._params_obj, name, value)
                    return True
                break

        return result_flag
    