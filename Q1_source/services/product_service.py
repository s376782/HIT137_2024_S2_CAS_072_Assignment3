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