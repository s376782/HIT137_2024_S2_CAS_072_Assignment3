#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
from models.base_model import BaseModel

class Person(BaseModel):
    """
    Person class represents a person with attributes such as name, phone, email, salesperson status, and city.
    Inherits from BaseModel and implements the abstract method get_data() to return the person's data as a list.
    """

    def __init__(self, name, phone, email, saleperson, city):
        """
        Initializes the Person object with the given attributes.

        Args:
            name (str): The name of the person.
            phone (str): The phone number of the person.
            email (str): The email address of the person.
            saleperson (str): The name of the sale person
            city (str): The city where the person lives.
        """

        self.name = name
        '''(public) The name of the person.'''
        self.phone = phone
        '''(public) The phone number of the person.'''
        self.email = email
        '''(public) The email address of the person.'''
        self.saleperson = saleperson
        '''(public) The name of the sale person'''
        self.city = city
        '''(public) The city where the person lives.'''

    def get_data(self) -> list:
        """
        (public) Returns the person's data as a list.

        Returns:
            list: A list containing the person's name, phone, email, salesperson status, and city.
        """
        return [self.name, self.phone, self.email, self.saleperson, self.city]
