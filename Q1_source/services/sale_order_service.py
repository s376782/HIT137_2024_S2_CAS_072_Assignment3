from typing import override
from models.so import SO
from services.base_service import BaseService

class SaleOrderService(BaseService[SO]):
    Source = 'data/SaleOrder.xlsx'

    def __init__(self):
        super().__init__(SaleOrderService.Source)

    @override
    def add(self, model: SO):
        return super().add(model)

    def get_top_customers(self, head=10):
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
        '''Get unique sale person names and grouped totals

        :param int head: quantity to take

        :returns: tuple (X, Y)
            - X: Sale person names
            - Y: Corresponding totals
        '''
        top_saleperson = self._df.groupby('Sale person')['Total'].sum().sort_values(ascending=False).head(head)
        X = top_saleperson.index
        Y = top_saleperson.values
        return X, Y
    
    def get_total_amount(self):
        return self._df["Total"].sum()

    def get_number_of_customers(self):
        return self._df["Customer name"].nunique()

    def get_top_regular_customer(self):
        top_customer = self._df.groupby('Customer name')['Total'].sum().idxmax()
        max_amount = self._df.groupby('Customer name')['Total'].sum().max()
        return top_customer, max_amount
    
    def get_top_sale_person(self):
        top_salesperson = self._df.groupby('Sale person')['Total'].sum().idxmax()  #find sale person
        max_sales_amount = self._df.groupby('Sale person')['Total'].sum().max()  # Lấy tổng doanh số của người đó
        return top_salesperson, max_sales_amount