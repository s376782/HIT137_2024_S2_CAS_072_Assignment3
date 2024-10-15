import tkinter as tk
from tkinter import messagebox, ttk
from services.purchase_order_service import PurchaseOrderService
from models.po import PO
from pages.base_page import BasePage
from constants import bg0_color, fg0_color

class PurchaseOrderPage(BasePage):
    def __init__(self, parent, controller, purchase_order_service: PurchaseOrderService):
        super().__init__(parent, controller)

        self.__purchase_order_service = purchase_order_service

        # Define colors
        bg3_color = "#3CB371"  # Medium sea green for background
        fg3_color = "#ffffff"  # White text remains unchanged
        btn3_color = "#32CD32"  # Lime green for buttons

        # Set the background color of the main window
        self.configure(bg=bg3_color)
        frame3 = tk.LabelFrame(self, text="Purchase Orders", bg=bg3_color, fg=fg3_color, font=("Helvetica", 16, "bold"))
        frame3.place(rely=0, relx=0, height=700, width=1900)

        # This is a treeview.
        self.__tv3 = ttk.Treeview(frame3)
        column_list_account = ["Purchase number", "Creation date", "Vendor name", "Buyer", "Total"]
        self.__tv3['columns'] = column_list_account
        self.__tv3["show"] = "headings"  # removes empty column
        for column in column_list_account:
            self.__tv3.heading(column, text=column)
            self.__tv3.column(column, width=50)
        self.__tv3.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame3)
        treescroll.configure(command=self.__tv3.yview)
        self.__tv3.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")

        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.66, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Total Purchase Order: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 9, "bold"))
        self.__total_label1.place(rely=0.7, relx=0.02)

        #Count data total
        self.total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        self.total_label2.place(rely=0.74, relx=0.02)

        #Count Total vendor
        self.total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        self.total_label3.place(rely=0.78, relx=0.02)

        #Count Top 1 regular vendor
        self.total_label4 = tk.Label(self, text="Top regular vendor: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        self.total_label4.place(rely=0.82, relx=0.02)

        #Count Top buyer
        self.total_label5 = tk.Label(self, text="Top buyer: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        self.total_label5.place(rely=0.86, relx=0.02)

        # Button to open the popup for adding a new product
        add_PO_button = tk.Button(self, text="Add new purchase order", command=self.__open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_PO_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window

        self.__load_data()

    def __load_data(self):
        # Convert the DataFrame to a list of lists (as expected by Treeview)
        data = self.__purchase_order_service.values()

        for row in data:
            self.__tv3.insert("", "end", values=row)

        # total
        # Count number of PO
        self.__total_label1.config(text=f"- Total Purchase Order: {len(data)}")

        # Count total amount
        total_amount = self.__purchase_order_service.get_total_amount()
        self.total_label2.config(text=f"- Total amount: {total_amount}")

        # Get number of customers have orders
        total_customer = self.__purchase_order_service.get_number_of_customers()
        self.total_label3.config(text=f"- Total customer have orders: {total_customer}")

        #Get Top 1 regular customer
        top_vendor, max_amount = self.__purchase_order_service.get_top_regular_customer()
        self.total_label4.config(text=f"- Top vendor: {top_vendor} with amount: {max_amount}")

        #Get Top 1 buyer

        top_buyer, max_buying_amount = self.__purchase_order_service.get_top_buyer()
        self.total_label5.config(text=f"- Top Sales person: {top_buyer} with sales amount: {max_buying_amount}")

    def __refresh_data(self):
        # Deletes the data in the current treeview and reinserts it.
        self.__tv3.delete(*self.__tv3.get_children())  # *=splat operator
        self.__load_data()

    def __open_popup(self):
        # Create a new popup window
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Purchase Order")  # Set the window title
        self.__popup.geometry("600x500")  # Set the size of the self.__popup window

        # Labels and entry fields for product name, type, and sale price
        tk.Label(self.__popup, text="PO number").pack(pady=5)  # Label for product name
        self.__POnumber_entry = tk.Entry(self.__popup)  # Entry field for product name
        self.__POnumber_entry.pack(pady=5)

        tk.Label(self.__popup, text="Creation date").pack(pady=5)  # Label for product type
        self.__CreateDate_entry = tk.Entry(self.__popup)  # Entry field for product type
        self.__CreateDate_entry.pack(pady=5)

        tk.Label(self.__popup, text="Vendor name").pack(pady=5)  # Label for sale price
        self.__VendorName_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__VendorName_entry.pack(pady=5)

        tk.Label(self.__popup, text="Buyer").pack(pady=5)  # Label for sale price
        self.__Buyer_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__Buyer_entry.pack(pady=5)

        tk.Label(self.__popup, text="Total").pack(pady=5)  # Label for sale price
        self.__Total_entry = tk.Entry(self.__popup)  # Entry field for sale price
        self.__Total_entry.pack(pady=5)

        # Save button in the popup window
        tk.Button(self.__popup, text="Save", command=self.__save_PO).pack(pady=20)  # Button to trigger save action

    # Function to save the new product to the Excel file
    def __save_PO(self):
        try:
            po = PO(self.__POnumber_entry.get(),
                    self.__CreateDate_entry.get(),
                    self.__VendorName_entry.get(),
                    self.__Buyer_entry.get(),
                    int(self.__Total_entry.get()))
            # Get the data entered by the user
            new_PO = po.get_data()

            # Validate if all fields are filled
            if not all(new_PO):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                return

            self.__purchase_order_service.add(new_PO)

            # Refresh the Treeview to show the newly added product
            self.__refresh_data()

            # Close the self.__popup window after saving the product
            self.__popup.destroy()
        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save Sale Order: {e}")

