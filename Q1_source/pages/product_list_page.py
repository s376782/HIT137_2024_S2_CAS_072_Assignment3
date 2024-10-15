import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from models.product import Product
from pages.base_page import BasePage
from constants import frame_styles, bg0_color, fg0_color

class ProductListPage(BasePage):  # inherits from the GUI class

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Define the path to the Excel file as an instance variable
        self.file_path = "data/Product.xlsx"  # Set self.file_path here

        # Define colors
        bg_color = "#3b5998"  # blue
        fg_color = "#ffffff"  # White text
        btn_color = "#4267B2"  # Slightly lighter blue for buttons

        # Set the background color of the main window
        self.configure(bg=bg_color)

        # Product list frame
        frame1 = tk.LabelFrame(self, text="Product list", bg=bg_color, fg=fg_color, font=("Helvetica", 16, "bold"))
        frame1.place(rely=0.0, relx=0, height=700, width=1900)

        # This is a treeview.
        tv1 = ttk.Treeview(frame1)
        column_list_account = ["Name", "Type", "Sale price"]
        tv1['columns'] = column_list_account
        tv1["show"] = "headings"  # removes empty column
        for column in column_list_account:
            tv1.heading(column, text=column)
            tv1.column(column, width=50)
        tv1.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame1)
        treescroll.configure(command=tv1.yview)
        tv1.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")


        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        #Count data total
        total_label1 = tk.Label(self, text="Total Products: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        total_label1.place(rely=0.74, relx=0.02)

        #Count data total
        total_label2 = tk.Label(self, text="Total Type: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        total_label2.place(rely=0.78, relx=0.02)

        #Count data total
        total_label3 = tk.Label(self, text="Max price product: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        total_label3.place(rely=0.82, relx=0.02)

        #Count data total
        total_label4 = tk.Label(self, text="Min price product: 0", bg="#FFFFFF", fg = "#2b3d6e", font=("Arial", 11, "bold"))
        total_label4.place(rely=0.86, relx=0.02)


        def Load_data():

            # Read the data from the Excel file
            file_path = "data/Product.xlsx"
            df = pd.read_excel(file_path)  # Assuming the file has the required columns

                # Convert the DataFrame to a list of lists (as expected by Treeview)
            product_list1 = df.values.tolist()

            for row in product_list1:
                tv1.insert("", "end", values=row)


            # Create the label and configure it
            #Count product
            total_label1.config(text=f"- Total Product: {len(product_list1)}")

            #Count type
            total_label2.config(text=f"- Total Type: {df["Type"].nunique()}")

            # Get max price product
            max_price_index = df['Price'].idxmax()  # index of max price product
            max_price_product_name = df.iloc[max_price_index]['Name']
            max_price_product_price = df.iloc[max_price_index]['Price']
            total_label3.config(text=f"- Max price product: {max_price_product_name} with price: {max_price_product_price:.2f}")

            # Get min price product
            min_price_index = df['Price'].idxmin()  # index of min price product
            min_price_product_name = df.iloc[min_price_index]['Name']
            min_price_product_price = df.iloc[min_price_index]['Price']
            total_label4.config(text=f"- Min price product: {min_price_product_name} with price: {min_price_product_price:.2f}")

    # Include other methods like Refresh_data, open_popup, etc.
        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it
            tv1.delete(*tv1.get_children())  # *=splat operator
            Load_data()

        Load_data()

        def open_popup():
            # Create a new popup window
            popup = tk.Toplevel(self)
            popup.title("Add New Product")  # Set the window title
            popup.geometry("400x300")  # Set the size of the popup window

            # Labels and entry fields for product name, type, and sale price
            tk.Label(popup, text="Product Name").pack(pady=5)  # Label for product name
            name_entry = tk.Entry(popup)  # Entry field for product name
            name_entry.pack(pady=5)

            tk.Label(popup, text="Product Type").pack(pady=5)  # Label for product type
            type_entry = tk.Entry(popup)  # Entry field for product type
            type_entry.pack(pady=5)

            tk.Label(popup, text="Sale Price").pack(pady=5)  # Label for sale price
            price_entry = tk.Entry(popup)  # Entry field for sale price
            price_entry.pack(pady=5)

            # Function to save the new product to the Excel file
            def save_product():
                product = Product(name_entry.get(), type_entry.get(), price_entry.get())
                # Get the data entered by the user
                new_product = [
                    product.get_name(),  # Get the product name
                    product.type,  # Get the product type
                    product.saleprice  # Get the sale price
                ]

                # Validate if all fields are filled
                if not all(new_product):
                    messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                    return

                try:
                    # Read the existing Excel data into a pandas DataFrame
                    df = pd.read_excel(self.file_path)

                    # Append the new product to the DataFrame
                    df.loc[len(df)] = new_product

                    # Save the updated DataFrame back to the Excel file
                    df.to_excel(self.file_path, index=False)

                    # Refresh the Treeview to show the newly added product
                    Refresh_data()

                    # Close the popup window after saving the product
                    popup.destroy()

                except Exception as e:
                    # Show error message if saving fails
                    messagebox.showerror("Error", f"Failed to save product: {e}")

            # Save button in the popup window
            tk.Button(popup, text="Save", command=save_product).pack(pady=20)  # Button to trigger save action

        # Button to open the popup for adding a new product
        add_product_button = tk.Button(self, text="Add New Product", command=open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_product_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window