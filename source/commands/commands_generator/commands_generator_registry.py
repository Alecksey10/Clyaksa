import abc

class CommandsGeneratorRegistry(abc.ABCMeta):
    
    def __init__(cls, name, bases, namespace):
        super(CommandsGeneratorRegistry, cls).__init__(name, bases, namespace)
        

        if(not hasattr(cls, "get_generator_name")):
            raise Exception("class does not have get_generator_name method")
        else:
            if(not bool(cls.__abstractmethods__)):
                #Регестрируем новый алгоритм
                if(getattr(CommandsGeneratorRegistry, 'registred_classes', None)):
                    CommandsGeneratorRegistry.registred_classes.append(cls)
                else:
                    CommandsGeneratorRegistry.registred_classes = [cls]
                print(CommandsGeneratorRegistry.registred_classes) 

    @classmethod
    def get_registered_generators(cls):
        return cls.registred_classes
    
    @classmethod
    def get_registered_generators_names(cls):
        result = []
        for cc in cls.registred_classes:
            result.append(cc.get_generator_name())
        return result
        
    
    def __new__(cls, name, bases, dct:dict):
        return super().__new__(cls, name, bases, dct)