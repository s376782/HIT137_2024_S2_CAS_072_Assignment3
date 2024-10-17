from typing import override
from models.so import SO
from services.base_service import BaseService

class SaleOrderService(BaseService[SO]):
    """
    SaleOrderService class handles operations related to sales orders. It extends the BaseService class
    and interacts with sales order data stored in an Excel file.
    """

    __source = 'data/SaleOrder.xlsx'
    '''(private) Path to the Excel file storing sales orders.'''

    def __init__(self):
        """
        Initializes the SaleOrderService by loading sales order data from the Excel file.
        """
        super().__init__(SaleOrderService.__source)

    @override
    def add(self, model: SO):
        """
        (public) Overrides the add method to add a new sales order.

        Args:
            model (SO): The sales order model to be added.
        """
        return super().add(model)

    def get_top_customers(self, head=10):
        """
        (public) Get top customer names and their corresponding totals, sorted by total amount.

        Args:
            head (int): The number of top customers to return.

        Returns:
            tuple: A tuple containing:
                - X (list of strings): Customer names.
                - Y (list of floats): Corresponding totals.
        """
        '''Get top 10 customer names and grouped totals

        :param int head: quantity to take

        :returns: tuple (X, Y)
            - X: Customer names
            - Y: Corresponding totals
        '''
        top_customers = self._df.groupby('Customer name')['Total'].sum().sort_values(ascending=False).head(head)
        X = top_customers.index  # Customer names
        Y = top_customers.values  # Corresponding totals
        return X, Y

    def get_top_sale_persons(self, head=10):
        """
        (public) Get top salesperson names and their corresponding totals, sorted by total amount.

        Args:
            head (int): The number of top salespersons to return.

        Returns:
            tuple: A tuple containing:
                - X (list of strings): Salesperson names.
                - Y (list of floats): Corresponding totals.
        """
        top_saleperson = self._df.groupby('Sale person')['Total'].sum().sort_values(ascending=False).head(head)
        X = top_saleperson.index
        Y = top_saleperson.values
        return X, Y
    
    def get_total_amount(self):
        """
        (public) Returns the total sum of all sales orders.

        Returns:
            float: The total amount of all sales orders.
        """
        return self._df["Total"].sum()

    def get_number_of_customers(self):
        """
        (public) Returns the total number of unique customers.

        Returns:
            int: The number of unique customers.
        """
        return self._df["Customer name"].nunique()

    def get_top_regular_customer(self):
        """
        (public) Returns the customer with the highest total order amount.

        Returns:
            tuple: A tuple containing:
                - top_customer (str): The customer name.
                - max_amount (float): The maximum total amount for the top customer.
        """
        top_customer = self._df.groupby('Customer name')['Total'].sum().idxmax()
        max_amount = self._df.groupby('Customer name')['Total'].sum().max()
        return top_customer, max_amount
    
    def get_top_sale_person(self):
        """
        (public) Returns the salesperson with the highest total sales amount.

        Returns:
            tuple: A tuple containing:
                - top_salesperson (str): The salesperson name.
                - max_sales_amount (float): The maximum sales amount for the top salesperson.
        """
        top_salesperson = self._df.groupby('Sale person')['Total'].sum().idxmax()
        max_sales_amount = self._df.groupby('Sale person')['Total'].sum().max()
        return top_salesperson, max_sales_amount