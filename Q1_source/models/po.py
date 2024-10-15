from typing import override
from models.base_model import BaseModel

class PO(BaseModel):
    # __init__ is known as the constructor
    def __init__(self, name, date, vendor, buyer, total):
        self.name = name
        self.date = date
        self.vendor = vendor
        self.buyer = buyer
        self.total = total

    def get_name(self):
        return "PO" + str(super().get_name())
    
    @override
    def get_data(self) -> list:
        return [self.name, self.date, self.vendor, self.buyer, self.total]