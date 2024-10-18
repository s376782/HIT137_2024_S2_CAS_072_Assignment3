#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
from typing import override
from models.base_model import BaseModel

class PO(BaseModel):
    """
    PO class represents a Purchase Order with attributes such as name, date, vendor, buyer, and total.
    Inherits from BaseModel and implements the get_data method to return the purchase order's data as a list.
    """

    def __init__(self, name, date, vendor, buyer, total):
        """
        Initializes the PO (Purchase Order) object with the given attributes.

        Args:
            name (str): The name of the purchase order.
            date (str): The creation date of the purchase order.
            vendor (str): The vendor associated with the purchase order.
            buyer (str): The buyer associated with the purchase order.
            total (float): The total amount of the purchase order.
        """

        self.name = name
        '''(public) The name of the purchase order.'''
        self.date = date
        '''(public) The creation date of the purchase order.'''
        self.vendor = vendor
        '''(public) The vendor associated with the purchase order.'''
        self.buyer = buyer
        '''(public) The buyer associated with the purchase order.'''
        self.total = total
        '''(public) The total amount of the purchase order.'''
    
    @override
    def get_data(self) -> list:
        """
        (public) Returns the purchase order's data as a list.

        Returns:
            list: A list containing the purchase order's name, date, vendor, buyer, and total amount.
        """
        return [self.name, self.date, self.vendor, self.buyer, self.total]