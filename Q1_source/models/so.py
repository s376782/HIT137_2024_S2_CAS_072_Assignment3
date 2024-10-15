from models.base_model import BaseModel

class SO(BaseModel):
    # __init__ is known as the constructor
    def __init__(self, name, date, cusname, saleperson, total):
        self.name = name
        self.date = date
        self.cusname = cusname
        self.saleperson = saleperson
        self.total = total

    def get_name(self):
        return "SO" + str(super().get_name())