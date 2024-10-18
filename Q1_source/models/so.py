#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
from models.base_model import BaseModel

class SO(BaseModel):
    """
    SO class represents a Sales Order with attributes such as name, date, customer name,
    salesperson, and total. Inherits from BaseModel and implements the abstract method get_data.
    """

    def __init__(self, name, date, cusname, saleperson, total):
        """
        Initializes the Sales Order (SO) object with the given attributes.

        Args:
            name (str): The name of the sales order.
            date (str): The creation date of the sales order.
            cusname (str): The customer name for the sales order.
            saleperson (str): The salesperson responsible for the sales order.
            total (float): The total amount of the sales order.
        """
        self.name = name
        '''(public) The name of the sales order.'''
        self.date = date
        '''(public) The creation date of the sales order.'''
        self.cusname = cusname
        '''(public) The customer name for the sales order.'''
        self.saleperson = saleperson
        '''(public) The salesperson responsible for the sales order.'''
        self.total = total
        '''(public) The total amount of the sales order.'''

    def get_data(self) -> list:
        """
        (public) Returns the sales order's data as a list.

        Returns:
            list: A list containing the sales order's name, date, customer name, salesperson, and total amount.
        """
        return [self.name, self.date, self.cusname, self.saleperson, self.total]
