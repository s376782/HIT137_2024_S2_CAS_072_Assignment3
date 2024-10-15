import pandas as pd
from numpy import ndarray
from abc import ABC
from typing import Generic, TypeVar
from models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseService(ABC, Generic[T]):
    '''
    '''

    def __init__(self, file):
        self._file = file
        self._df = pd.read_excel(file)
        ''''''

    def values(self) -> list:
        '''
        '''
        return self._df.values.tolist()

    def add(self, model: T):
        '''
        '''
        # Append the new product to the DataFrame
        self._df.loc[len(self._df)] = model

        # Save the updated DataFrame back to the Excel file
        self._df.to_excel(self._file, index=False)
