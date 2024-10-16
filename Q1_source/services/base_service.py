import pandas as pd
from abc import ABC
from typing import Generic, TypeVar
from models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseService(ABC, Generic[T]):
    """
    BaseService is a generic service class for handling data operations on models that 
    extend from BaseModel. It provides basic methods to load, retrieve, and add data 
    from an Excel file.
    """

    def __init__(self, file):
        """
        Initializes the BaseService with a file path and loads the data from an Excel file 
        into a DataFrame.
        
        Args:
            file: Path to the Excel file.
        """

        self.__file = file
        '''(private) Path to the Excel file storing the data.'''
        self._df = pd.read_excel(file)
        '''(protected) Pandas DataFrame holding the data loaded from the Excel file.'''

    def values(self) -> list:
        """
        (public) Returns all the values from the DataFrame as a list of lists.
        
        Returns:
            A list of rows, where each row is represented as a list of column values.
        """
        return self._df.values.tolist()

    def add(self, model: T):
        """
        (public) Adds a new record to the DataFrame, representing a new model instance.
        
        Args:
            model: An instance of the model extending BaseModel that needs to be added 
                   to the DataFrame.
        """
        # Convert the model object into a DataFrame row and append it to the existing data.
        self._df.loc[len(self._df)] = model.get_data()

        # Save the updated DataFrame back to the Excel file.
        self._df.to_excel(self.__file, index=False)
