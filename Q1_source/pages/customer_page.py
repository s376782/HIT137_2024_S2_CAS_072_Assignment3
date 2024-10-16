import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from services.customer_service import CustomerService
from models.person import Person
from pages.base_page import BasePage
from constants import frame_styles, bg0_color, fg0_color

class CustomerPage(BasePage):
    def __init__(self, parent, controller, customer_service: CustomerService):
        super().__init__(parent, controller)

        self.__customer_service = customer_service

        bg2_color = "#FFD700"  # Gold (Yellow) background
        fg2_color = "#000000"  # Black text

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame = tk.LabelFrame(self, frame_styles, text="Customer", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0, relx=0, height=700, width=1900)

        # This is a treeview.
        self.__tv = ttk.Treeview(frame)
        columns = ["Name", "Phone", "Email", "Saleperson", "City"]
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

        #Summary
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold"))
        total_label.place(rely=0.7, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Customer: 0", bg="#FFFFFF", fg = "#000000", font=("Arial", 11, "bold"))
        self.__total_label1.place(rely=0.74, relx=0.02)

        # Button to open the popup for adding a new product
        add_product_button = tk.Button(self, text="Add New Customer", command=self.__open_pop,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_product_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window
        
        self.__load_data()

    def __load_data(self):
        
        data = self.__customer_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        self.__total_label1.config(text=f"Total customer: {len(data)}")

    def __refresh_data(self):
        # Deletes the data in the current treeview and reinserts it
        self.__tv.delete(*self.__tv.get_children())  # *=splat operator
        self.__load_data()

    def __open_pop(self):
        # Create a new self.__popup window
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Customer")  # Set the window title
        self.__popup.geometry("600x500")  # Set the size of the self.__popup window

        # Labels and entry fields for product name, type, and sale price
        tk.Label(self.__popup, text="Customer Name").pack(pady=5)  # Label for product name
        self.__name_entry = tk.Entry(self.__popup)  # Entry field for product name
        self.__name_entry.pack(pady=5)

        tk.Label(self.__popup, text="Phone").pack(pady=5)  # Label for product type
        self.__phone_entry = tk.Entry(self.__popup)  # Entry field for product type
        self.__phone_entry.pack(pady=5)

        tk.Label(self.__popup, text="Email").pack(pady=5)  # Label for sale price
        self.__email_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__email_entry.pack(pady=5)

        tk.Label(self.__popup, text="Sale person").pack(pady=5)  # Label for sale price
        self.__saleperson_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__saleperson_entry.pack(pady=5)

        tk.Label(self.__popup, text="City").pack(pady=5)  # Label for sale price
        self.__city_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__city_entry.pack(pady=5)

        # Save button in the self.__popup window
        tk.Button(self.__popup, text="Save", command=self.__save_customer).pack(pady=20)  # Button to trigger save action

    def __save_customer(self):
        try:
            # Get the data entered by the user
            new_person = Person(self.__name_entry.get(),
                                self.__phone_entry.get(),
                                self.__email_entry.get(),
                                self.__saleperson_entry.get(),
                                self.__city_entry.get())

            new_customer = new_person.get_data()
            if not all(new_customer):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                return

            self.__customer_service.add(new_customer)
            self.__refresh_data()

            # Close the self.__popup window after saving the product
            self.__popup.destroy()

        except Exception as f:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save customer: {f}")
