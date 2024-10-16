import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from tkinter import Tk
from typing import override
from signup_window import ISignupCallback, SignupWindow
from main_window import MainWindow
from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from login_window import ILoginCallback, LoginWindow
from services.purchase_order_service import PurchaseOrderService

class Application(ILoginCallback, ISignupCallback):
    '''
    '''

    def __init__(self):
        self.__product_service = ProductService()
        self.__purchase_order_service = PurchaseOrderService()
        self.__sale_order_service = SaleOrderService()
        self.__active_window = None

    @override
    def on_login_success(self, username: str):
        self.__run_window(
            MainWindow(self.__product_service,
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
        # self.__run_window(LoginWindow(self))
        self.on_login_success('')

    def __run_window(self, window: Tk):
        if self.__active_window:
            self.__active_window.destroy()
        self.__active_window = window
        self.__active_window.mainloop()

if __name__ == "__main__":
    Application().run()
