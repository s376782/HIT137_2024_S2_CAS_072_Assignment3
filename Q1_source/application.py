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
    """
    Application class manages the lifecycle of the application's windows and handles 
    transitions between login, signup, and main application pages.
    
    Implements ILoginCallback and ISignupCallback interfaces to handle user actions 
    related to login and signup events.
    """

    def __init__(self):
        """
        Initializes the Application class by setting up the required services 
        and initializing window management.
        """
        self.__customer_service = CustomerService()
        self.__product_service = ProductService()
        self.__purchase_order_service = PurchaseOrderService()
        self.__sale_order_service = SaleOrderService()
        self.__active_window = None

    @override
    def on_login_success(self, username: str):
        """
        Callback triggered upon successful login.
        
        Args:
            username (str): The username of the logged-in user.
        """
        self.__run_window(
            MainWindow(self.__customer_service,
                       self.__product_service,
                       self.__purchase_order_service,
                       self.__sale_order_service)
        )

    @override
    def on_open_signup(self):
        """
        Callback triggered to open the signup window.
        """
        self.__run_window(SignupWindow(self))

    @override
    def on_signup(self):
        """
        Callback triggered after a successful signup, returning the user to the login window.
        """
        self.__run_window(LoginWindow(self))

    def run(self):
        """
        Starts the application by opening the login window.
        """
        self.__run_window(LoginWindow(self))

    def __run_window(self, window: Tk):
        """
        (private) Manages the transition between windows by destroying the active window 
        and starting a new one.

        Args:
            window (Tk): The new window to display.
        """
        if self.__active_window:
            self.__active_window.destroy() # Close the current active window
        self.__active_window = window      # Set the new active window
        self.__active_window.mainloop()    # Start the new window's main loop
