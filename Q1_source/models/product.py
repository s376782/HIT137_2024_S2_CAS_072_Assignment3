#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
from models.base_model import BaseModel

class Product(BaseModel):
    """
    Product class represents a product with attributes such as name, type, and sale price.
    Inherits from BaseModel and implements the get_data method to return the product's data as a list.
    """

    def __init__(self, name, type, saleprice):
        """
        Initializes the Product object with the given attributes.

        Args:
            name (str): The name of the product.
            type (str): The type or category of the product.
            saleprice (float): The sale price of the product.
        """

        self.name = name
        '''(public) The name of the product.'''
        self.type = type
        '''(public) The type or category of the product.'''
        self.saleprice = saleprice
        '''(public) The sale price of the product.'''

    def get_data(self) -> list:
        """
        (public) Returns the product's data as a list.

        Returns:
            list: A list containing the product's name, type, and sale price.
        """
        return [self.name, self.type, self.saleprice]
