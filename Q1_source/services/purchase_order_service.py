from models.po import PO
from services.base_service import BaseService

class PurchaseOrderService(BaseService[PO]):
    __Source = 'data/PurchaseOrder.xlsx'

    def __init__(self):
        super().__init__(PurchaseOrderService.__Source)

    def get_top_venders(self, head=10):
        '''Get unique vendor names and grouped totals

        :param int head: quantity to take

        :returns: tuple (X, Y)
            - X: Vendor names
            - Y: Corresponding totals
        '''
        top_vendor = self._df.groupby('Vendor name')['Total'].sum().sort_values(ascending=False).head(10)
        X = top_vendor.index
        Y = top_vendor.values
        return X, Y

    def get_total_amount(self):
        return self._df["Total"].sum()

    def get_number_of_customers(self):
        return self._df["Vendor name"].nunique()

    def get_top_regular_customer(self):
        top_vendor = self._df.groupby('Vendor name')['Total'].sum().idxmax()  #find sale person
        max_amount = self._df.groupby('Vendor name')['Total'].sum().max()  # Lấy tổng doanh số của người đó
        return top_vendor, max_amount
    
    def get_top_buyer(self):
        top_buyer = self._df.groupby('Buyer')['Total'].sum().idxmax()  #find sale person
        max_buying_amount = self._df.groupby('Buyer')['Total'].sum().max()  # Lấy tổng doanh số của người đó
        return top_buyer, max_buying_amount