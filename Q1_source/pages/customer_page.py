import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from models.person import Person
from pages.base_page import BasePage
from constants import frame_styles, bg0_color, fg0_color

class CustomerPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.file_path2 = "data/Customer.xlsx"  # Set self.file_path here

        bg2_color = "#FFD700"  # Gold (Yellow) background
        fg2_color = "#000000"  # Black text
        btn2_color = "#FFC300"  # Light yellow for buttons

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame4 = tk.LabelFrame(self, frame_styles, text="Customer", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame4.place(rely=0, relx=0, height=700, width=1900)
        tv4 = ttk.Treeview(frame4)
        column_list_account = ["Name", "Phone", "Email", "Saleperson", "City"]
        tv4['columns'] = column_list_account
        tv4["show"] = "headings"  # removes empty column
        for column in column_list_account:
            tv4.heading(column, text=column)
            tv4.column(column, width=50)
        tv4.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame4)
        treescroll.configure(command=tv4.yview)
        tv4.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")

        #Summary
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold"))
        total_label.place(rely=0.7, relx=0.02)

        total_label1 = tk.Label(self, text="Customer: 0", bg="#FFFFFF", fg = "#000000", font=("Arial", 11, "bold"))
        total_label1.place(rely=0.74, relx=0.02)

        def Load_data():
              # Read the data from the Excel file
            file_path2 = "data/Customer.xlsx"
            df = pd.read_excel(file_path2)  # Assuming the file has the required columns

                # Convert the DataFrame to a list of lists (as expected by Treeview)
            customer = df.values.tolist()

            for row in customer:
                tv4.insert("", "end", values=row)
            total_label1.config(text=f"Total customer: {len(customer)}")

        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it
            tv4.delete(*tv4.get_children())  # *=splat operator
            Load_data()

        Load_data()
        def open_popup():
            # Create a new popup window
            popup = tk.Toplevel(self)
            popup.title("Add New Customer")  # Set the window title
            popup.geometry("600x500")  # Set the size of the popup window

            # Labels and entry fields for product name, type, and sale price
            tk.Label(popup, text="Customer Name").pack(pady=5)  # Label for product name
            name_entry = tk.Entry(popup)  # Entry field for product name
            name_entry.pack(pady=5)

            tk.Label(popup, text="Phone").pack(pady=5)  # Label for product type
            phone_entry = tk.Entry(popup)  # Entry field for product type
            phone_entry.pack(pady=5)

            tk.Label(popup, text="Email").pack(pady=5)  # Label for sale price
            email_entry = tk.Entry(popup)  # Entry field for sale price
            email_entry.pack(pady=5)

            tk.Label(popup, text="Sale person").pack(pady=5)  # Label for sale price
            saleperson_entry = tk.Entry(popup)  # Entry field for sale price
            saleperson_entry.pack(pady=5)

            tk.Label(popup, text="City").pack(pady=5)  # Label for sale price
            city_entry = tk.Entry(popup)  # Entry field for sale price
            city_entry.pack(pady=5)

            # Function to save the new product to the Excel file
            def save_customer():
                # Get the data entered by the user
                new_person = Person(name_entry.get(), phone_entry.get(), email_entry.get(), saleperson_entry.get(), city_entry.get())
                new_customer = [
                    new_person.get_name(),  # Get the product name
                    new_person.phone,  # Get the product type
                    new_person.email,
                    new_person.saleperson,# Get the sale person
                    new_person.city
                ]

                # Validate if all fields are filled
                if not all(new_customer):
                    messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                    return

                try:
                    # Read the existing Excel data into a pandas DataFrame
                    df = pd.read_excel(self.file_path2)

                    # Append the new product to the DataFrame
                    df.loc[len(df)] = new_customer

                    # Save the updated DataFrame back to the Excel file
                    df.to_excel(self.file_path2, index=False)

                    # Refresh the Treeview to show the newly added product
                    Refresh_data()

                    # Close the popup window after saving the product
                    popup.destroy()

                except Exception as f:
                    # Show error message if saving fails
                    messagebox.showerror("Error", f"Failed to save customer: {f}")

            # Save button in the popup window
            tk.Button(popup, text="Save", command=save_customer).pack(pady=20)  # Button to trigger save action

        # Button to open the popup for adding a new product
        add_product_button = tk.Button(self, text="Add New Customer", command=open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_product_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window