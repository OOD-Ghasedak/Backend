from typing import TypeVar, Type, Generic

T = TypeVar('T')


class Configurer(Generic[T]):

    def configure_class(self) -> Type[T]:
        raise NotImplementedError

    def configure(self, *args, **kwargs) -> T:
        raise NotImplementedError
