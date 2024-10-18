#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
import tkinter as tk

from pages.dashboard_page import DashboardPage
from pages.product_list_page import ProductListPage
from pages.purchase_order_page import PurchaseOrderPage
from pages.sale_order_page import SaleOrderPage
from pages.customer_page import CustomerPage

class MenuBar(tk.Menu):
    """
    MenuBar class defines the top-level navigation bar for the application. It includes menus 
    for Dashboard, Sale, Purchase, Product, and Customer pages, allowing the user to switch 
    between these pages using menu commands.
    """

    def __init__(self, master):
        """
        Initializes the MenuBar and sets up all the menus and their corresponding commands.

        Args:
            master: The root window or parent widget to attach the MenuBar to.
        """
        super().__init__(master)

        # Define a bold font for the menu items
        bold_font = ('Arial', 10, 'bold')

        # Dashboard Menu
        menu_dashboard = tk.Menu(self, tearoff=0)
        self.add_cascade(label="DASHBOARD", menu=menu_dashboard)
        menu_dashboard.add_command(label="DASHBOARD", command=lambda: master.show_page(DashboardPage), font=bold_font)

        # Sale Menu
        menu_sale = tk.Menu(self, tearoff=0)
        self.add_cascade(label="SALE", menu=menu_sale)
        menu_sale.add_command(label="SALE ORDER", command=lambda: master.show_page(SaleOrderPage), font=bold_font)

        # Purchase Menu
        menu_purchase = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PURCHASE", menu=menu_purchase)
        menu_purchase.add_command(label="PURCHASE ORDER", command=lambda: master.show_page(PurchaseOrderPage), font=bold_font)

        # Product Menu
        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PRODUCT", menu=menu_file)
        menu_file.add_command(label="LIST OF PRODUCT", command=lambda: master.show_page(ProductListPage), font=bold_font)

        # Contact (Customer) Menu
        menu_contact = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CONTACT", menu=menu_contact)
        menu_contact.add_command(label="LIST OF CUSTOMER", command=lambda: master.show_page(CustomerPage), font=bold_font)