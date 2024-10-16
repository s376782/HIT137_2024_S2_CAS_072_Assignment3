from tkinter import Tk
from typing import override

from login_window import ILoginCallback, LoginWindow
from main_window import MainWindow
from services.customer_service import CustomerService
from services.product_service import ProductService
from services.purchase_order_service import PurchaseOrderService
from services.sale_order_service import SaleOrderService
from signup_window import ISignupCallback, SignupWindow

class Application(ILoginCallback, ISignupCallback):
    '''
    '''

    def __init__(self):
        self.__customer_service = CustomerService()
        self.__product_service = ProductService()
        self.__purchase_order_service = PurchaseOrderService()
        self.__sale_order_service = SaleOrderService()
        self.__active_window = None

    @override
    def on_login_success(self, username: str):
        self.__run_window(
            MainWindow(self.__customer_service,
                       self.__product_service,
                       self.__purchase_order_service,
                       self.__sale_order_service)
        )

    @override
    def on_open_signup(self):
        self.__run_window(SignupWindow(self))

    @override
    def on_signup(self):
        self.__run_window(LoginWindow(self))

    def run(self):
        self.__run_window(LoginWindow(self))
        # self.on_login_success('')

    def __run_window(self, window: Tk):
        if self.__active_window:
            self.__active_window.destroy()
        self.__active_window = window
        self.__active_window.mainloop()