from typing import override
from models.product import Product
from services.base_service import BaseService

class ProductService(BaseService[Product]):
    Source = 'data/Product.xlsx'

    def __init__(self):
        super().__init__(ProductService.Source)

    @override
    def add(self, model: Product):
        return super().add(model)

    def get_type_report(self):
        labels = self._df["Type"].unique()
        counts = self._df.groupby("Type")["Name"].count()
        return (labels, counts)
    
    def get_total_type(self):
        return self._df["Type"].nunique()

    def get_max_price_product(self):
        index = self._df['Price'].idxmax()
        name = self._df.iloc[index]['Name']
        price = self._df.iloc[index]['Price']
        return name, price

    def get_min_price_product(self):
        index = self._df['Price'].idxmin()
        name = self._df.iloc[index]['Name']
        price = self._df.iloc[index]['Price']
        return name, price
