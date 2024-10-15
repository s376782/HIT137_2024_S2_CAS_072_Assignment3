from models.person import Person
from services.base_service import BaseService

class CustomerService(BaseService[Person]):
    __Source = 'data/Customer.xlsx'

    def __init__(self):
        super().__init__(CustomerService.__Source)
