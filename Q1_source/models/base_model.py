from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    BaseModel serves as an abstract base class for models, enforcing a contract
    that any subclass must implement the get_data() method.
    
    Subclasses should implement get_data() to return the model's data as a list.
    """

    @abstractmethod
    def get_data(self) -> list:
        """
        Abstract method that should be implemented by any subclass of BaseModel.
        
        This method is expected to return the model's data as a list.
        
        Returns:
            list: The data of the model in list form.
        
        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method.")
