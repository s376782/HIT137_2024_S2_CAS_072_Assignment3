#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
import tkinter as tk
from tkinter import messagebox, ttk
from services.purchase_order_service import PurchaseOrderService
from models.po import PO
from pages.base_page import BasePage
from constants import bg0_color, fg0_color

class PurchaseOrderPage(BasePage):
    """
    PurchaseOrderPage class represents the UI page for managing purchase orders.
    It displays purchase order data, and provides functionality to add new purchase orders via a popup window.
    """

    def __init__(self, parent, controller, purchase_order_service: PurchaseOrderService):
        """
        Initializes the PurchaseOrderPage UI components and loads purchase order data.

        Args:
            parent: The parent widget.
            controller: The controller managing page transitions.
            purchase_order_service: Service to interact with purchase order data.
        """
        super().__init__(parent, controller)

        self.__purchase_order_service = purchase_order_service
        '''(private) Service to interact with purchase order data.'''

        # Define colors for the UI
        bg3_color = "#3CB371"  # Medium sea green for background
        fg3_color = "#ffffff"  # White text remains unchanged

        # Set the background color of the main window
        self.configure(bg=bg3_color)

        # Create a labeled frame to contain the purchase orders
        frame = tk.LabelFrame(self, text="Purchase Orders", bg=bg3_color, fg=fg3_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0, relx=0, height=self._screen_height- self._screen_height/2.75, width=self._screen_width - 10)

        # Create a Treeview widget for displaying the purchase orders
        self.__tv = ttk.Treeview(frame)
        '''(private) Treeview widget for displaying the purchase orders'''
        columns = ["Purchase number", "Creation date", "Vendor name", "Buyer", "Total"]
        self.__tv['columns'] = columns
        self.__tv["show"] = "headings"  # Remove the default empty first column
        for column in columns:
            self.__tv.heading(column, text=column)  # Set column headings
            self.__tv.column(column, width=50)  # Set default width for each column
        self.__tv.place(relheight=1, relwidth=0.995)  # Fill the treeview in the frame

        # Add a scrollbar to the treeview
        treescroll = tk.Scrollbar(frame)
        treescroll.configure(command=self.__tv.yview)
        self.__tv.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")  # Position the scrollbar on the right side

        # Labels for displaying summary data
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Total Purchase Order: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        '''(private) Label for displaying total purchase order'''
        self.__total_label1.place(rely=0.74, relx=0.02)

        self.__total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        '''(private) Label for displaying total amount of all orders'''
        self.__total_label2.place(rely=0.78, relx=0.02)

        self.__total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the number of unique vendors'''
        self.__total_label3.place(rely=0.82, relx=0.02)

        self.__total_label4 = tk.Label(self, text="Top regular vendor: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the top vendor with the highest total order amount'''
        self.__total_label4.place(rely=0.86, relx=0.02)

        self.__total_label5 = tk.Label(self, text="Top buyer: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the top buyer with the highest total purchase amount'''
        self.__total_label5.place(rely=0.9, relx=0.02)

        # Button to open the popup for adding a new purchase order
        add_PO_button = tk.Button(self, text="Add new purchase order", command=self.__open_popup, bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_PO_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window

        # Load purchase order data into the Treeview and update summary labels
        self.__load_data()

    def __load_data(self):
        """
        (private) Loads purchase order data into the Treeview and updates the summary labels.
        """
        # Fetch purchase order data as a list of lists
        data = self.__purchase_order_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        # Update summary labels based on the loaded data
        self.__total_label1.config(text=f"- Total Purchase Order: {len(data)}")
        self.__total_label2.config(text=f"- Total amount: {self.__purchase_order_service.get_total_amount()}")
        self.__total_label3.config(text=f"- Total customer have orders: {self.__purchase_order_service.get_number_of_customers()}")

        # Get and display the top vendor and the top buyer
        top_vendor, max_amount = self.__purchase_order_service.get_top_regular_customer()
        self.__total_label4.config(text=f"- Top vendor: {top_vendor} with amount: {max_amount}")

        top_buyer, max_buying_amount = self.__purchase_order_service.get_top_buyer()
        self.__total_label5.config(text=f"- Top Sales person: {top_buyer} with sales amount: {max_buying_amount}")

    def __refresh_data(self):
        """
        (private) Clears the current Treeview and reloads the data.
        """
        self.__tv.delete(*self.__tv.get_children()) # Delete all current rows in the Treeview
        self.__load_data() # Reload the data and refresh the view

    def __open_popup(self):
        """
        (private) Opens a popup window for adding a new purchase order.
        """
        # Create a new popup window
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Purchase Order")  # Set the window title
        self.__popup.geometry("600x500")  # Set the window size

        # Create labels and entry fields for the popup window
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

    def __save_PO(self):
        """
        (private) Saves the new purchase order and refreshes the Treeview data.
        """
        try:
            # Create a new PO object using the data from the entry fields
            po = PO(self.__POnumber_entry.get(),
                    self.__CreateDate_entry.get(),
                    self.__VendorName_entry.get(),
                    self.__Buyer_entry.get(),
                    int(self.__Total_entry.get()))

            # Get the data entered by the user and validate if all fields are filled
            new_PO = po.get_data()
            if not all(new_PO):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are missing
                return

            # Add the new purchase order to the service and refresh the Treeview
            self.__purchase_order_service.add(po)
            self.__refresh_data()

            # Close the popup window after successfully saving the purchase order
            self.__popup.destroy()

        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save Sale Order: {e}")

