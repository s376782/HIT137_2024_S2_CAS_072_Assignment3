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

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged
        btn2_color = "#A52A2A"  # Brownish red for buttons

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame2 = tk.LabelFrame(self, text="Sale Orders", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame2.place(rely=0, relx=0, height=700, width=1900)

        # This is a treeview.
        tv2 = ttk.Treeview(frame2)
        column_list_account = ["SO number", "Creation date", "Customer name", "Sale person", "Total"]
        tv2['columns'] = column_list_account
        tv2["show"] = "headings"  # removes empty column
        for column in column_list_account:
            tv2.heading(column, text=column)
            tv2.column(column, width=50)
        tv2.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame2)
        treescroll.configure(command=tv2.yview)
        tv2.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")

        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        total_label = tk.Label(self, text="Total Sale Order: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold") )
        total_label.place(rely=0.74, relx=0.02)

        #Count data total
        total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        total_label2.place(rely=0.78, relx=0.02)

        #Count Total customer have orders
        total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        total_label3.place(rely=0.82, relx=0.02)

        #Count Top 1 regular customer
        total_label4 = tk.Label(self, text="Top 1 regular customer: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        total_label4.place(rely=0.86, relx=0.02)

        #Count Top sale person
        total_label5 = tk.Label(self, text="Top sale person: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        total_label5.place(rely=0.90, relx=0.02)

        def Load_data():

        # Read the data from the Excel file
            file_path2 = "data/SaleOrder.xlsx"
            df = pd.read_excel(file_path2)  # Assuming the file has the required columns

                # Convert the DataFrame to a list of lists (as expected by Treeview)
            saleOrderlist = df.values.tolist()
            for row in saleOrderlist:
                tv2.insert("", "end", values=row)
            #Count total sale order
            total_label.config(text=f"- Total Sale Order: {len(saleOrderlist)}")

            #Count total amount
            total_label2.config(text=f"- Total amount: {df["Total"].sum()}")

            #Get number of customers have orders
            total_label3.config(text=f"- Total customer have orders: {df["Customer name"].nunique()}")

            #Get Top 1 regular customer
            top_customer = df.groupby('Customer name')['Total'].sum().idxmax()  #find sale person
            max_amount = df.groupby('Customer name')['Total'].sum().max()  # Lấy tổng doanh số của người đó
            total_label4.config(text=f"- Top customer: {top_customer} with amount: {max_amount}")

            #Get Top 1 sale person
            top_salesperson = df.groupby('Sale person')['Total'].sum().idxmax()  #find sale person
            max_sales_amount = df.groupby('Sale person')['Total'].sum().max()  # Lấy tổng doanh số của người đó
            total_label5.config(text=f"- Top Sales person: {top_salesperson} with sales amount: {max_sales_amount}")


        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it.
            tv2.delete(*tv2.get_children())  # *=splat operator
            Load_data()

        Load_data()

        def open_popup():
            # Create a new popup window
            popup = tk.Toplevel(self)
            popup.title("Add New Sale Order")  # Set the window title
            popup.geometry("600x500")  # Set the size of the popup window

            # Labels and entry fields for product name, type, and sale price
            tk.Label(popup, text="SO number").pack(pady=5)  # Label for product name
            SOnumber_entry = tk.Entry(popup)  # Entry field for product name
            SOnumber_entry.pack(pady=5)

            tk.Label(popup, text="Creation date").pack(pady=5)  # Label for product type
            CreateDate_entry = tk.Entry(popup)  # Entry field for product type
            CreateDate_entry.pack(pady=5)

            tk.Label(popup, text="Customer name").pack(pady=5)  # Label for sale price
            CusName_entry = tk.Entry(popup)  # Entry field for sale price
            CusName_entry.pack(pady=5)

            tk.Label(popup, text="Sale person").pack(pady=5)  # Label for sale price
            Saleperson_entry = tk.Entry(popup)  # Entry field for sale price
            Saleperson_entry.pack(pady=5)

            tk.Label(popup, text="Total").pack(pady=5)  # Label for sale price
            Total_entry = tk.Entry(popup)  # Entry field for sale price
            Total_entry.pack(pady=5)

            # Function to save the new product to the Excel file
            def save_SO():
                SaleOrder = SO(SOnumber_entry.get(), CreateDate_entry.get(), CusName_entry.get(), Saleperson_entry.get(), Total_entry.get())
                # Get the data entered by the user
                new_SO = [
                    SaleOrder.get_name(),  # Get the SOnumber
                    SaleOrder.date,  # Get the creation date
                    SaleOrder.cusname,  # Get the SOnumber
                    SaleOrder.date, # Get the creation date
                    SaleOrder.total
                ]

                # Validate if all fields are filled
                if not all(new_SO):
                    messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                    return

                try:
                    # Read the existing Excel data into a pandas DataFrame
                    df = pd.read_excel(self.file_path2)

                    # Append the new product to the DataFrame
                    df.loc[len(df)] = new_SO

                    # Save the updated DataFrame back to the Excel file
                    df.to_excel(self.file_path2, index=False)

                    # Refresh the Treeview to show the newly added product
                    Refresh_data()

                    # Close the popup window after saving the product
                    popup.destroy()

                except Exception as e:
                    # Show error message if saving fails
                    messagebox.showerror("Error", f"Failed to save Sale Order: {e}")

            # Save button in the popup window
            tk.Button(popup, text="Save", command=save_SO).pack(pady=20)  # Button to trigger save action

        # Button to open the popup for adding a new product
        add_SO_button = tk.Button(self, text="Add New Sale Order", command=open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_SO_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window