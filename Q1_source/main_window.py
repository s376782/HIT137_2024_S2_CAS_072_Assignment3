from decorators import authorized, timing
from menu_bar import MenuBar
from pages.customer_page import CustomerPage
from pages.dashboard_page import DashboardPage
from pages.product_list_page import ProductListPage
from pages.purchase_order_page import PurchaseOrderPage
from pages.sale_order_page import SaleOrderPage
from services.customer_service import CustomerService
from services.product_service import ProductService
from services.purchase_order_service import PurchaseOrderService
from services.sale_order_service import SaleOrderService

from tkinter import Tk

class MainWindow(Tk):
    """
    MainWindow class extends Tkinter's Tk and serves as the main application window, 
    managing multiple pages such as Dashboard, Sale Order, Purchase Order, Product List, and Customer pages.

    It utilizes a dictionary to store instances of pages and switches between them based on user interaction.
    """

    def __init__(self,
                 customer_service: CustomerService,
                 product_service: ProductService,
                 purchase_order_service: PurchaseOrderService,
                 sale_order_service: SaleOrderService):
        """
        Initializes the MainWindow with different services and sets up the application layout.

        Args:
            customer_service (CustomerService): The service to manage customer data.
            product_service (ProductService): The service to manage product data.
            purchase_order_service (PurchaseOrderService): The service to manage purchase order data.
            sale_order_service (SaleOrderService): The service to manage sale order data.
        """
        super().__init__()

        # Dictionary to hold page frames
        self.__frames = {
            SaleOrderPage: SaleOrderPage(self, self, sale_order_service),
            PurchaseOrderPage: PurchaseOrderPage(self, self, purchase_order_service),
            ProductListPage: ProductListPage(self, self, product_service),
            CustomerPage: CustomerPage(self, self, customer_service),
            DashboardPage: DashboardPage(self, self, sale_order_service, purchase_order_service, product_service),
        }
        '''(private) Holds all the page frames.'''

        # Configure and display each frame in the grid layout
        for frame in self.__frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Create and configure the MenuBar
        menubar = MenuBar(self)
        self.config(menu=menubar)

    @timing
    @authorized
    def show_page(self, page_class):
        """
        (public) Method to show a specific page based on its name.
        
        Args:
            name (str): The name of the page to display.
        """
        frame = self.__frames.get(page_class)
        if frame:
            frame.tkraise()
        else:
            raise ValueError(f"Page '{page_class.__name__}' not found.")
