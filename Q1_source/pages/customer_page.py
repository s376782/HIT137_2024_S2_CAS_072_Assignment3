import tkinter as tk
from tkinter import messagebox, ttk
from services.customer_service import CustomerService
from models.person import Person
from pages.base_page import BasePage
from constants import frame_styles, bg0_color, fg0_color

class CustomerPage(BasePage):
    """
    CustomerPage class represents the UI page for managing customer data.
    It displays customer information, allows adding new customers, and provides summary data.
    """

    def __init__(self, parent, controller, customer_service: CustomerService):
        """
        Initializes the CustomerPage UI components and loads customer data.

        Args:
            parent: The parent widget.
            controller: The controller managing page transitions.
            customer_service: Service to interact with customer data.
        """
        super().__init__(parent, controller)
        self.__customer_service = customer_service
        '''(private) Service to interact with customer data.'''

        bg2_color = "#FFD700"  # Gold (Yellow) background
        fg2_color = "#000000"  # Black text

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        # Create a labeled frame for displaying customer data
        frame = tk.LabelFrame(self, frame_styles, text="Customer", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame.place(rely=0, relx=0, height=self._screen_height- self._screen_height/2.75, width=self._screen_width - 10)

        # Create a Treeview widget for displaying the customer information
        self.__tv = ttk.Treeview(frame)
        '''(private) Treeview widget to display customer data.'''
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

        # Summary label
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold"))
        total_label.place(rely=0.7, relx=0.02)

        # Display total customers label
        self.__total_label1 = tk.Label(self, text="Customer: 0", bg="#FFFFFF", fg = "#000000", font=("Arial", 11, "bold"))
        '''(private) Label to display total number of customers.'''
        self.__total_label1.place(rely=0.74, relx=0.02)

        # Button to open the popup for adding a new customer
        add_product_button = tk.Button(self, text="Add New Customer", command=self.__open_pop,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_product_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window
        
        # Load customer data into the Treeview
        self.__load_data()

    def __load_data(self):
        """
        (private) Loads customer data into the Treeview and updates the summary label.
        """
        data = self.__customer_service.values()

        # Insert data into the Treeview
        for row in data:
            self.__tv.insert("", "end", values=row)

        # Update the total customers label
        self.__total_label1.config(text=f"Total customer: {len(data)}")

    def __refresh_data(self):
        """
        (private) Refreshes the customer data displayed in the Treeview.
        Deletes current data and reloads it.
        """
        self.__tv.delete(*self.__tv.get_children())  # Delete all rows
        self.__load_data()  # Reload the data

    def __open_pop(self):
        """
        (private) Opens a popup window for adding a new customer.
        """
        # Create a new popup window
        self.__popup = tk.Toplevel(self)
        self.__popup.title("Add New Customer")  # Set the window title
        self.__popup.geometry("600x500")  # Set the size of the self.__popup window

        # Labels and entry fields for product name, type, and sale price
        tk.Label(self.__popup, text="Customer Name").pack(pady=5)  # Label for product name
        self.__name_entry = tk.Entry(self.__popup)  # Entry field for product name
        self.__name_entry.pack(pady=5)

        # Labels and entry fields for customer data
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
        """
        (private) Saves the new customer data entered in the popup window.
        """
        try:
            # Get the data entered by the user
            new_person = Person(self.__name_entry.get(),
                                self.__phone_entry.get(),
                                self.__email_entry.get(),
                                self.__saleperson_entry.get(),
                                self.__city_entry.get())

            new_customer = new_person.get_data()

            # Check if all fields are filled
            if not all(new_customer):
                messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                return

            # Add new customer to the service and refresh the data
            self.__customer_service.add(new_person)
            self.__refresh_data()

            # Close the self.__popup window after saving the product
            self.__popup.destroy()

        except Exception as e:
            # Show error message if saving fails
            messagebox.showerror("Error", f"Failed to save customer: {e}")
