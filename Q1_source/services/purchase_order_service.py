from models.po import PO
from services.base_service import BaseService

class PurchaseOrderService(BaseService[PO]):
    __Source = 'data/PurchaseOrder.xlsx'
    '''(private) Path to the Excel file for purchase orders.'''

    def __init__(self):
        """
        Initializes the PurchaseOrderService by loading the purchase orders from the Excel file.
        """
        super().__init__(PurchaseOrderService.__Source)

    def get_top_venders(self, head=10):
        """
        (public) Get unique vendor names and their corresponding totals, sorted by total amount.

        Args:
            head (int): The number of top vendors to return.

        Returns:
            tuple: A tuple containing two elements:
                - X: Vendor names (list of strings).
                - Y: Corresponding totals (list of floats).
        """
        top_vendor = self._df.groupby('Vendor name')['Total'].sum().sort_values(ascending=False).head(10)
        X = top_vendor.index.tolist()
        Y = top_vendor.values.tolist()
        return X, Y

    def get_total_amount(self):
        """
        (public) Returns the total sum of all purchase orders.

        Returns:
            float: The total amount of all purchase orders.
        """
        return self._df["Total"].sum()

    def get_number_of_customers(self):
        """
        (public) Returns the total number of unique vendors (customers).

        Returns:
            int: The number of unique vendors.
        """
        return self._df["Vendor name"].nunique()

    def get_top_regular_customer(self):
        """
        (public) Returns the top regular customer (vendor) by the total amount.

        Returns:
            tuple: A tuple containing:
                - top_vendor (str): The vendor name.
                - max_amount (float): The maximum total amount for the top vendor.
        """
        top_vendor = self._df.groupby('Vendor name')['Total'].sum().idxmax()
        max_amount = self._df.groupby('Vendor name')['Total'].sum().max()
        return top_vendor, max_amount
    
    def get_top_buyer(self):
        """
        (public) Returns the top buyer by total purchase amount.

        Returns:
            tuple: A tuple containing:
                - top_buyer (str): The buyer name.
                - max_buying_amount (float): The maximum purchase amount for the top buyer.
        """
        top_buyer = self._df.groupby('Buyer')['Total'].sum().idxmax()
        max_buying_amount = self._df.groupby('Buyer')['Total'].sum().max()
        return top_buyer, max_buying_amount