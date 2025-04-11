import abc

class AlgorithmsRegistry(abc.ABCMeta):
    
    def __init__(cls, name, bases, namespace):
        super(AlgorithmsRegistry, cls).__init__(name, bases, namespace)
        

        if(not hasattr(cls, "get_algorithm_name")):
            raise Exception("class does not have get_algorithm_name method")
        else:
            if(not bool(cls.__abstractmethods__)):
                #Регестрируем новый алгоритм
                if(getattr(AlgorithmsRegistry, 'registred_classes', None)):
                    AlgorithmsRegistry.registred_classes.append(cls)
                else:
                    AlgorithmsRegistry.registred_classes = [cls]
                print(AlgorithmsRegistry.registred_classes) 

    @classmethod
    def get_registered_algorithms(cls):
        return cls.registred_classes
    
    @classmethod
    def get_registered_algorithms_names(cls):
        result = []
        for cc in cls.registred_classes:
            result.append(cc.get_algorithm_name())
        return result
        
    
    def __new__(cls, name, bases, dct:dict):
        return super().__new__(cls, name, bases, dct)