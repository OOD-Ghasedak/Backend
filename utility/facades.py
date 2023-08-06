from abc import ABC


class ComponentFacade(ABC):

    @classmethod
    def get_instance(cls):
        return cls()
