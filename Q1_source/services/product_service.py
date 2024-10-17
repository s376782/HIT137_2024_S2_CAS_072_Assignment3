from typing import override
from models.product import Product
from services.base_service import BaseService

class ProductService(BaseService[Product]):
    """
    ProductService class handles operations related to products. It extends the BaseService class
    and interacts with product data stored in an Excel file.
    """

    __Source = 'data/Product.xlsx'
    '''(private) Path to the Excel file storing product data.'''

    def __init__(self):
        """
        Initializes the ProductService by loading product data from the Excel file.
        """
        super().__init__(ProductService.__Source)

    def get_type_report(self):
        """
        (public) Generates a report of the different product types and their counts.

        Returns:
            tuple: A tuple containing:
                - labels (ndarray): An array of unique product types.
                - counts (Series): The number of products for each type.
        """
        labels = self._df["Type"].unique()
        counts = self._df.groupby("Type")["Name"].count()
        return (labels, counts)
    
    def get_total_type(self):
        """
        (public) Returns the total number of unique product types.

        Returns:
            int: The number of unique product types.
        """
        return self._df["Type"].nunique()

    def get_max_price_product(self):
        """
        (public) Retrieves the product with the highest price.

        Returns:
            tuple: A tuple containing:
                - name (str): The name of the product with the highest price.
                - price (float): The price of the product.
        """
        index = self._df['Price'].idxmax()
        name = self._df.iloc[index]['Name']
        price = self._df.iloc[index]['Price']
        return name, price

    def get_min_price_product(self):
        """
        (public) Retrieves the product with the lowest price.

        Returns:
            tuple: A tuple containing:
                - name (str): The name of the product with the lowest price.
                - price (float): The price of the product.
        """
        index = self._df['Price'].idxmin()
        name = self._df.iloc[index]['Name']
        price = self._df.iloc[index]['Price']
        return name, price
