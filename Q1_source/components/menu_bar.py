from Shop_management import Customer, Dashboard, Productlist, PurchaseOrder, SaleOrder


import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        # Define a bold font for the menu items
        bold_font = ('Arial', 10, 'bold')

        menu_dashboard = tk.Menu(self, tearoff=0)
        self.add_cascade(label="DASHBOARD", menu=menu_dashboard)
        menu_dashboard.add_command(label="DASHBOARD", command=lambda: parent.show_frame(Dashboard), font=bold_font)

        menu_sale = tk.Menu(self, tearoff=0)
        self.add_cascade(label="SALE", menu=menu_sale)
        menu_sale.add_command(label="SALE ORDER", command=lambda: parent.show_frame(SaleOrder), font=bold_font)

        menu_purchase = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PURCHASE", menu=menu_purchase)
        menu_purchase.add_command(label="PURCHASE ORDER", command=lambda: parent.show_frame(PurchaseOrder), font=bold_font)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PRODUCT", menu=menu_file)
        menu_file.add_command(label="LIST OF PRODUCT", command=lambda: parent.show_frame(Productlist), font=bold_font)


        menu_contact = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CONTACT", menu=menu_contact)
        menu_contact.add_command(label="LIST OF CUSTOMER", command=lambda: parent.show_frame(Customer), font=bold_font)