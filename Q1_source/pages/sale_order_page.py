import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from services.sale_order_service import SaleOrderService
from models.so import SO
from pages.base_page import BasePage
from constants import bg0_color, fg0_color

class SaleOrderPage(BasePage):
    def __init__(self, parent, controller, sale_order_service: SaleOrderService):
        super().__init__(parent, controller)

        self.__sale_order_service = sale_order_service

        # Define colors for the UI
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame = tk.LabelFrame(self, text="Sale Orders", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0, relx=0, height=700, width=1900)

        # This is a treeview.
        self.__tv = ttk.Treeview(frame)
        columns = ["SO number", "Creation date", "Customer name", "Sale person", "Total"]
        self.__tv['columns'] = columns
        self.__tv["show"] = "headings"  # removes empty column
        for column in columns:
            self.__tv.heading(column, text=column)
            self.__tv.column(column, width=50)
        self.__tv.place(relheight=1, relwidth=0.995)

        treescroll = tk.Scrollbar(frame)
        treescroll.configure(command=self.__tv.yview)
        self.__tv.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")

        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Total Sale Order: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold") )
        self.__total_label1.place(rely=0.74, relx=0.02)

        #Count data total
        self.__total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        self.__total_label2.place(rely=0.78, relx=0.02)

        #Count Total customer have orders
        self.__total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        self.__total_label3.place(rely=0.82, relx=0.02)

        #Count Top 1 regular customer
        self.__total_label4 = tk.Label(self, text="Top 1 regular customer: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        self.__total_label4.place(rely=0.86, relx=0.02)

        #Count Top sale person
        self.__total_label5 = tk.Label(self, text="Top sale person: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        self.__total_label5.place(rely=0.90, relx=0.02)

        # Button to open the popup for adding a new product
        add_SO_button = tk.Button(self, text="Add New Sale Order", command=self.__open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_SO_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window

        self.__load_data()

    def __load_data(self):
        data = self.__sale_order_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        # Update summary labels based on the loaded data
        self.__total_label1.config(text=f"- Total Sale Order: {len(data)}")
        self.__total_label2.config(text=f"- Total amount: {self.__sale_order_service.get_total_amount()}")
        self.__total_label3.config(text=f"- Total customer have orders: {self.__sale_order_service.get_number_of_customers()}")

        #Get Top 1 regular customer
        top_customer, max_amount = self.__sale_order_service.get_top_regular_customer()
        self.__total_label4.config(text=f"- Top customer: {top_customer} with amount: {max_amount}")

        #Get Top 1 sale person
        top_salesperson, max_sales_amount = self.__sale_order_service.get_top_sale_person()
        self.__total_label5.config(text=f"- Top Sales person: {top_salesperson} with sales amount: {max_sales_amount}")


    def __refresh_data(self):
        """
        (private) Clears the current Treeview and reloads the data.
        """
        self.__tv.delete(*self.__tv.get_children()) # Delete all current rows in the Treeview
        self.__load_data() # Reload the data and refresh the view


    def __open_popup(self):
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Sale Order")  # Set the window title
        self.__popup.geometry("600x500")  # Set the size of the self.__popup window

        # Labels and entry fields for product name, type, and sale price
        tk.Label(self.__popup, text="SO number").pack(pady=5)  # Label for product name
        self.__SOnumber_entry = tk.Entry(self.__popup)  # Entry field for product name
        self.__SOnumber_entry.pack(pady=5)

        tk.Label(self.__popup, text="Creation date").pack(pady=5)  # Label for product type
        self.__CreateDate_entry = tk.Entry(self.__popup)  # Entry field for product type
        self.__CreateDate_entry.pack(pady=5)

        tk.Label(self.__popup, text="Customer name").pack(pady=5)  # Label for sale price
        self.__CusName_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__CusName_entry.pack(pady=5)

        tk.Label(self.__popup, text="Sale person").pack(pady=5)  # Label for sale price
        self.__Saleperson_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__Saleperson_entry.pack(pady=5)

        tk.Label(self.__popup, text="Total").pack(pady=5)  # Label for sale price
        self.__Total_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__Total_entry.pack(pady=5)

        # Save button in the self.__popup window
        tk.Button(self.__popup, text="Save", command=self.__save_SO).pack(pady=20)  # Button to trigger save action

    def __save_SO(self):
        try:
            so = SO(self.__SOnumber_entry.get(),
                    self.__CreateDate_entry.get(),
                    self.__CusName_entry.get(),
                    self.__Saleperson_entry.get(),
                    int(self.__Total_entry.get()))

            # Get the data entered by the user
            new_SO = so.get_data()
            if not all(new_SO):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                return

            self.__sale_order_service.add(new_SO)
            self.__refresh_data()

            # Close the self.__popup window after saving the product
            self.__popup.destroy()

        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save Sale Order: {e}")
