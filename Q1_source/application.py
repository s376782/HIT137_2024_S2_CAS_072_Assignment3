from tkinter import Frame, Tk

from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from pages.dashboard_page import DashboardPage
from pages.product_list_page import ProductListPage
from pages.purchase_order_page import PurchaseOrderPage
from pages.sale_order_page import SaleOrderPage
from pages.customer_page import CustomerPage
from login_window import ILoginCallback
from menu_bar import MenuBar
from services.purchase_order_service import PurchaseOrderService

class MainWindow(Tk, ILoginCallback):
    '''
    Class Application has a multiple inheritance (inherit Tk and ILoginCallback)
    '''
    def __init__(self,
                 product_service: ProductService,
                 purchase_order_service: PurchaseOrderService,
                 sale_order_service: SaleOrderService):
        super().__init__()

        # main_frame = Frame(self, bg="#FFF0F5", height=800, width=1900)
        # main_frame.pack_propagate(0)
        # main_frame.pack(fill="both", expand="true")
        # main_frame.grid_rowconfigure(0, weight=1)
        # main_frame.grid_columnconfigure(0, weight=1)

        self.__frames = {
            SaleOrderPage.__name__: SaleOrderPage(self, self, sale_order_service),
            PurchaseOrderPage.__name__: PurchaseOrderPage(self, self, purchase_order_service),
            ProductListPage.__name__: ProductListPage(self, self),
            CustomerPage.__name__: CustomerPage(self, self),
            DashboardPage.__name__: DashboardPage(self, self, sale_order_service, purchase_order_service, product_service),
        }
        '''__frame variable is private encapsulation'''

        for frame in self.__frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        menubar = MenuBar(self)
        self.config(menu=menubar)

    def show_page(self, name):
        '''
        (public method encapsulation)
        Show page base on name
        '''
        frame = self.__frames[name]
        frame.tkraise()