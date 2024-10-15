from models.base_model import BaseModel

class Person(BaseModel):
    # __init__ is known as the constructor
    def __init__(self, name, phone, email, saleperson, city):
        self.name = name
        self.phone = phone
        self.email = email
        self.saleperson = saleperson
        self.city = city