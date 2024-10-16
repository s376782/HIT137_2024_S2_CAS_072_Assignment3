import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from services.product_service import ProductService
from models.product import Product
from pages.base_page import BasePage
from constants import bg0_color, fg0_color

class ProductListPage(BasePage):

    def __init__(self, parent, controller, product_service: ProductService):
        super().__init__(parent, controller)

        self.__product_service = product_service

        # Define colors
        bg_color = "#3b5998"  # blue
        fg_color = "#ffffff"  # White text

        # Set the background color of the main window
        self.configure(bg=bg_color)

        # Product list frame
        frame = tk.LabelFrame(self, text="Product list", bg=bg_color, fg=fg_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0.0, relx=0, height=700, width=1900)

        # This is a treeview.
        self.__tv = ttk.Treeview(frame)
        columns = ["Name", "Type", "Sale price"]
        self.__tv['columns'] = columns
        self.__tv["show"] = "headings"  # removes empty column
        for column in columns:
            self.__tv.heading(column, text=column)
            self.__tv.column(column, width=50)
        self.__tv.place(relheight=1, relwidth=0.995)

        # Add a scrollbar to the treeview
        treescroll = tk.Scrollbar(frame)
        treescroll.configure(command=self.__tv.yview)
        self.__tv.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")  # Position the scrollbar on the right side

        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Total Products: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        self.__total_label1.place(rely=0.74, relx=0.02)

        self.__total_label2 = tk.Label(self, text="Total Type: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        self.__total_label2.place(rely=0.78, relx=0.02)

        self.__total_label3 = tk.Label(self, text="Max price product: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        self.__total_label3.place(rely=0.82, relx=0.02)

        self.__total_label4 = tk.Label(self, text="Min price product: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        self.__total_label4.place(rely=0.86, relx=0.02)

        # Button to open the popup for adding a new product
        add_product_button = tk.Button(self, text="Add New Product", command=self.__open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_product_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window

        self.__load_data()

    def __load_data(self):

        data = self.__product_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        # Update summary labels based on the loaded data
        self.__total_label1.config(text=f"- Total Product: {len(data)}")
        self.__total_label2.config(text=f"- Total Type: {self.__product_service.get_total_type()}")

        # Get max price product
        max_price_product_name, max_price_product_price = self.__product_service.get_max_price_product()
        self.__total_label3.config(text=f"- Max price product: {max_price_product_name} with price: {max_price_product_price:.2f}")

        # Get min price product
        min_price_product_name, min_price_product_price = self.__product_service.get_min_price_product()
        self.__total_label4.config(text=f"- Min price product: {min_price_product_name} with price: {min_price_product_price:.2f}")

    def __refresh_data(self):
        """
        (private) Clears the current Treeview and reloads the data.
        """
        self.__tv.delete(*self.__tv.get_children()) # Delete all current rows in the Treeview
        self.__load_data() # Reload the data and refresh the view

    def __open_popup(self):
        # Create a new self.__popup window
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Product")  # Set the window title
        self.__popup.geometry("400x300")  # Set the size of the self.__popup window

        # Labels and entry fields for product name, type, and sale price
        tk.Label(self.__popup, text="Product Name").pack(pady=5)  # Label for product name
        self.__name_entry = tk.Entry(self.__popup)  # Entry field for product name
        self.__name_entry.pack(pady=5)

        tk.Label(self.__popup, text="Product Type").pack(pady=5)  # Label for product type
        self.__type_entry = tk.Entry(self.__popup)  # Entry field for product type
        self.__type_entry.pack(pady=5)

        tk.Label(self.__popup, text="Sale Price").pack(pady=5)  # Label for sale price
        self.__price_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__price_entry.pack(pady=5)

        # Save button in the self.__popup window
        tk.Button(self.__popup, text="Save", command=self.__save_product).pack(pady=20)  # Button to trigger save action

    def __save_product(self):
        try:
            product = Product(self.__name_entry.get(),
                            self.__type_entry.get(),
                            float(self.__price_entry.get()))

            # Get the data entered by the user
            new_product = product.get_data()
            if not all(new_product):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                return

            self.__product_service.add(new_product)
            self.__refresh_data()

            # Close the self.__popup window after saving the product
            self.__popup.destroy()

        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save product: {e}")
