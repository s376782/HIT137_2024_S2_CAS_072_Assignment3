import tkinter as tk

from pages.dashboard_page import DashboardPage
from pages.product_list_page import ProductListPage
from pages.purchase_order_page import PurchaseOrderPage
from pages.sale_order_page import SaleOrderPage
from pages.customer_page import CustomerPage

class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        # Define a bold font for the menu items
        bold_font = ('Arial', 10, 'bold')

        menu_dashboard = tk.Menu(self, tearoff=0)
        self.add_cascade(label="DASHBOARD", menu=menu_dashboard)
        menu_dashboard.add_command(label="DASHBOARD", command=lambda: master.show_page(DashboardPage.__name__), font=bold_font)

        menu_sale = tk.Menu(self, tearoff=0)
        self.add_cascade(label="SALE", menu=menu_sale)
        menu_sale.add_command(label="SALE ORDER", command=lambda: master.show_page(SaleOrderPage.__name__), font=bold_font)

        menu_purchase = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PURCHASE", menu=menu_purchase)
        menu_purchase.add_command(label="PURCHASE ORDER", command=lambda: master.show_page(PurchaseOrderPage.__name__), font=bold_font)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PRODUCT", menu=menu_file)
        menu_file.add_command(label="LIST OF PRODUCT", command=lambda: master.show_page(ProductListPage.__name__), font=bold_font)

        menu_contact = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CONTACT", menu=menu_contact)
        menu_contact.add_command(label="LIST OF CUSTOMER", command=lambda: master.show_page(CustomerPage.__name__), font=bold_font)