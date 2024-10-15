from models.base_model import BaseModel

class Product(BaseModel):
    # __init__ is known as the constructor
    def __init__(self, name, type, saleprice):
        self.name = name
        self.type = type
        self.saleprice = saleprice