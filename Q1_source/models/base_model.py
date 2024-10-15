from abc import ABC, abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def get_data(self) -> list:
        raise NotImplementedError