import tkinter as tk
from tkinter import messagebox, ttk
from services.sale_order_service import SaleOrderService
from models.so import SO
from pages.base_page import BasePage
from constants import bg0_color, fg0_color

class SaleOrderPage(BasePage):
    """
    SaleOrderPage class represents the UI for managing sale orders. It allows users to view,
    add, and summarize sale orders using a Treeview widget.
    """

    def __init__(self, parent, controller, sale_order_service: SaleOrderService):
        """
        Initializes the SaleOrderPage UI components and loads sale order data.

        Args:
            parent: The parent widget.
            controller: The controller managing page transitions.
            sale_order_service: Service to interact with sale order data.
        """
        super().__init__(parent, controller)

        self.__sale_order_service = sale_order_service
        '''(private) Service to interact with sale order data.'''

        # Define colors for the UI
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        # Create a labeled frame for displaying sale orders
        frame = tk.LabelFrame(self, text="Sale Orders", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0, relx=0, height=self._screen_height- self._screen_height/2.75, width=self._screen_width - 10)

        # Create a Treeview widget for displaying the sale orders
        self.__tv = ttk.Treeview(frame)
        '''(private) Treeview widget for displaying sale orders.'''
        columns = ["SO number", "Creation date", "Customer name", "Sale person", "Total"]
        self.__tv['columns'] = columns
        self.__tv["show"] = "headings"  # Remove the empty column
        for column in columns:
            self.__tv.heading(column, text=column)
            self.__tv.column(column, width=50)
        self.__tv.place(relheight=1, relwidth=0.995)

        # Add a scrollbar to the Treeview
        treescroll = tk.Scrollbar(frame)
        treescroll.configure(command=self.__tv.yview)
        self.__tv.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")  # Position the scrollbar on the right side

        # Summary labels for total sales orders, total amount, etc.
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.7, relx=0.02)

        self.__total_label1 = tk.Label(self, text="Total Sale Order: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold") )
        '''(private) Label for displaying the total number of sale orders.'''
        self.__total_label1.place(rely=0.74, relx=0.02)

        self.__total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the total amount of all sale orders.'''
        self.__total_label2.place(rely=0.78, relx=0.02)

        self.__total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the total number of unique customers with orders.'''
        self.__total_label3.place(rely=0.82, relx=0.02)

        self.__total_label4 = tk.Label(self, text="Top 1 regular customer: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the top regular customer with the highest total order amount.'''
        self.__total_label4.place(rely=0.86, relx=0.02)

        self.__total_label5 = tk.Label(self, text="Top sale person: 0", bg="#FFFFFF", fg = "#8B0000", font=("Arial", 11, "bold"))
        '''(private) Label for displaying the top salesperson with the highest sales amount.'''
        self.__total_label5.place(rely=0.90, relx=0.02)

        # Button to open the popup for adding a new sale order
        add_SO_button = tk.Button(self, text="Add New Sale Order", command=self.__open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_SO_button.place(rely=0, relx=0.85)

        # Load sale order data into the Treeview
        self.__load_data()

    def __load_data(self):
        """
        (private) Loads sale order data into the Treeview and updates the summary labels.
        """
        data = self.__sale_order_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        # Update summary labels based on the loaded data
        self.__total_label1.config(text=f"- Total Sale Order: {len(data)}")
        self.__total_label2.config(text=f"- Total amount: {self.__sale_order_service.get_total_amount()}")
        self.__total_label3.config(text=f"- Total customer have orders: {self.__sale_order_service.get_number_of_customers()}")

        # Update Top 1 regular customer
        top_customer, max_amount = self.__sale_order_service.get_top_regular_customer()
        self.__total_label4.config(text=f"- Top customer: {top_customer} with amount: {max_amount}")

        # Update Top 1 salesperson
        top_salesperson, max_sales_amount = self.__sale_order_service.get_top_sale_person()
        self.__total_label5.config(text=f"- Top Sales person: {top_salesperson} with sales amount: {max_sales_amount}")


    def __refresh_data(self):
        """
        (private) Clears the current Treeview and reloads the data.
        """
        self.__tv.delete(*self.__tv.get_children())  # Delete all current rows in the Treeview
        self.__load_data()  # Reload the data

    def __open_popup(self):
        """
        (private) Opens a popup window for adding a new sale order.
        """
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Sale Order")  # Set the window title
        self.__popup.geometry("600x500")  # Set the window size

        # Labels and entry fields for sale order details
        tk.Label(self.__popup, text="SO number").pack(pady=5)
        self.__SOnumber_entry = tk.Entry(self.__popup)
        self.__SOnumber_entry.pack(pady=5)

        tk.Label(self.__popup, text="Creation date").pack(pady=5)
        self.__CreateDate_entry = tk.Entry(self.__popup)
        self.__CreateDate_entry.pack(pady=5)

        tk.Label(self.__popup, text="Customer name").pack(pady=5)
        self.__CusName_entry = tk.Entry(self.__popup)
        self.__CusName_entry.pack(pady=5)

        tk.Label(self.__popup, text="Sale person").pack(pady=5)
        self.__Saleperson_entry = tk.Entry(self.__popup)
        self.__Saleperson_entry.pack(pady=5)

        tk.Label(self.__popup, text="Total").pack(pady=5)
        self.__Total_entry = tk.Entry(self.__popup)
        self.__Total_entry.pack(pady=5)

        # Save button in the popup window
        tk.Button(self.__popup, text="Save", command=self.__save_SO).pack(pady=20)  # Button to trigger save action

    def __save_SO(self):
        """
        (private) Saves the new sale order entered in the popup window.
        """
        try:
            so = SO(self.__SOnumber_entry.get(),
                    self.__CreateDate_entry.get(),
                    self.__CusName_entry.get(),
                    self.__Saleperson_entry.get(),
                    int(self.__Total_entry.get()))

            # Validate if all fields are filled
            new_SO = so.get_data()
            if not all(new_SO):
                messagebox.showerror("Error", "All fields must be filled")
                return

            # Add the new sale order and refresh the Treeview
            self.__sale_order_service.add(new_SO)
            self.__refresh_data()

            # Close the popup window after saving the sale order
            self.__popup.destroy()

        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save Sale Order: {e}")
