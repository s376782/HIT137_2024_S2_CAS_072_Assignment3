from typing import override

from signup_window import SignupWindow
from main_window import MainWindow
from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from login_window import ILoginCallback, LoginWindow
from services.purchase_order_service import PurchaseOrderService

class Application(ILoginCallback):
    def __init__(self):
        self.__product_service = ProductService()
        self.__purchase_order_service = PurchaseOrderService()
        self.__sale_order_service = SaleOrderService()

    @override
    def onLoginSuccess(self, username: str):
        MainWindow(self.__product_service,
                   self.__purchase_order_service,
                   self.__sale_order_service).mainloop()

    @override
    def onSignup(self):
        SignupWindow(self).mainloop()

    def run(self):
        LoginWindow(self).mainloop()
