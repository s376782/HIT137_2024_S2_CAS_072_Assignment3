import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import openpyxl as op
import numpy as np


# You can also use a pandas dataframe
# you can convert the dataframe using df.to_numpy.tolist()

frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}


class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        self.geometry("626x431")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}

        text_styles = {"font": ("Verdana", 14),
                       "background": "blue",
                       "foreground": "#E1FFFF"}

        frame_login = tk.Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = tk.Label(frame_login, title_styles, text="Login")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: get_signup())
        signup_btn.place(rely=0.70, relx=0.75)

        def get_signup():
            SignupPage()

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                tk.messagebox.showinfo("Login Successful",
                                       "Welcome {}".format(username))
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username and line[3] == password:
                            return True
                    return False
            except FileNotFoundError:
                print("You need to Register first or amend Line 71 to if True:")
                return False


class SignupPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("250x150")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}

        label_user = tk.Label(main_frame, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(main_frame, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        # Define a bold font for the menu items
        bold_font = ('Arial', 10, 'bold')
        
        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PRODUCT", menu=menu_file)
        menu_file.add_command(label="LIST OF PRODUCT", command=lambda: parent.show_frame(Productlist), font=bold_font)


        menu_contact = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CONTACT", menu=menu_contact)
        menu_contact.add_command(label="LIST OF CUSTOMER", command=lambda: parent.show_frame(Customer), font=bold_font)

        menu_sale = tk.Menu(self, tearoff=0)
        self.add_cascade(label="SALE", menu=menu_sale)
        menu_sale.add_command(label="SALE ORDER", command=lambda: parent.show_frame(SaleOrder), font=bold_font)

        menu_purchase = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PURCHASE", menu=menu_purchase)
        menu_purchase.add_command(label="PURCHASE ORDER", command=lambda: parent.show_frame(PurchaseOrder), font=bold_font)
        
        menu_aiCheckTool = tk.Menu(self, tearoff=0)
        self.add_cascade(label="AI TOOL", menu=menu_aiCheckTool)
        menu_aiCheckTool.add_command(label="MATERIAL DETECTION", command=lambda: parent.show_frame(AItool), font=bold_font)
        menu_aiCheckTool.add_command(label="TRANSLATION", command=lambda: parent.show_frame(AItool), font=bold_font)


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        pages = (Productlist, SaleOrder, PurchaseOrder, Customer, AItool)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Productlist)
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        OpenNewWindow()

    def Quit_application(self):
        self.destroy()


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class Productlist(GUI):  # inherits from the GUI class
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        # Define the path to the Excel file as an instance variable
        self.file_path = "Product.xlsx"  # Set self.file_path here

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg_color = "#3b5998"  # blue
        fg_color = "#ffffff"  # White text
        btn_color = "#4267B2"  # Slightly lighter blue for buttons

        # Set the background color of the main window
        self.configure(bg=bg_color)

        frame1 = tk.LabelFrame(self, text="Product list", bg=bg_color, fg=fg_color, font=("Helvetica", 16, "bold"))
        frame1.place(rely=0.05, relx=0.02, height=550, width=1000)

 
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

        total_label = tk.Label(self, text="Total Products: 0")
        total_label.place(rely=0.8, relx=0.03)

        def Load_data():
        
            # Read the data from the Excel file
            file_path = "Product.xlsx"
            df = pd.read_excel(file_path)  # Assuming the file has the required columns
                
                # Convert the DataFrame to a list of lists (as expected by Treeview)
            product_list1 = df.values.tolist()
            
            for row in product_list1:
                tv1.insert("", "end", values=row)
            total_label.config(text=f"Total Products: {len(product_list1)}")
            
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
                # Get the data entered by the user
                new_product = [
                    name_entry.get(),  # Get the product name
                    type_entry.get(),  # Get the product type
                    price_entry.get()  # Get the sale price
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
        add_product_button = tk.Button(self, text="Add New Product", command=open_popup,  bg=bg_color, fg=fg_color, font=("Helvetica", 12, "bold"))
        add_product_button.place(rely=0.9, relx=0.03)  # Position the button at the bottom of the window


class SaleOrder(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        # Define the path to the Excel file as an instance variable
        self.file_path2 = "Sale Order.xlsx"  # Set self.file_path here

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged
        btn2_color = "#A52A2A"  # Brownish red for buttons

        # Set the background color of the main window
        self.configure(bg=bg2_color)
        
        frame2 = tk.LabelFrame(self, text="Sale Orders", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame2.place(rely=0.05, relx=0.02, height=550, width=1000)
        
        
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

        total_label = tk.Label(self, text="Total Sale Order: 0")
        total_label.place(rely=0.8, relx=0.03)
        
        def Load_data():
            
        # Read the data from the Excel file
            file_path2 = "Sale Order.xlsx"
            df = pd.read_excel(file_path2)  # Assuming the file has the required columns
                
                # Convert the DataFrame to a list of lists (as expected by Treeview)
            saleOrderlist = df.values.tolist()
            for row in saleOrderlist:
                tv2.insert("", "end", values=row)
            total_label.config(text=f"Total Sale Order: {len(saleOrderlist)}")
            
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
                # Get the data entered by the user
                new_SO = [
                    SOnumber_entry.get(),  # Get the SOnumber
                    CreateDate_entry.get(),  # Get the creation date
                    CusName_entry.get(),  # Get the customer name
                    Saleperson_entry.get(),  # Get the sale person
                    Total_entry.get() # Get the totoal amount of sale order
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
        add_SO_button = tk.Button(self, text="Add New Sale Order", command=open_popup,  bg=bg2_color, fg=fg2_color, font=("Helvetica", 12, "bold"))
        add_SO_button.place(rely=0.9, relx=0.03)  # Position the button at the bottom of the window


class PurchaseOrder(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
                # Define the path to the Excel file as an instance variable
        self.file_path3 = "Purchase order.xlsx"  # Set self.file_path here

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg3_color = "#3CB371"  # Medium sea green for background
        fg3_color = "#ffffff"  # White text remains unchanged
        btn3_color = "#32CD32"  # Lime green for buttons

        # Set the background color of the main window
        self.configure(bg=bg3_color)
        frame3 = tk.LabelFrame(self, text="Purchase Orders", bg=bg3_color, fg=fg3_color, font=("Helvetica", 16, "bold"))
        frame3.place(rely=0.05, relx=0.02, height=550, width=1000)
        
        # This is a treeview.
        tv3 = ttk.Treeview(frame3)
        column_list_account = ["Purchase number", "Creation date", "Vendor name", "Buyer", "Total"]
        tv3['columns'] = column_list_account
        tv3["show"] = "headings"  # removes empty column
        for column in column_list_account:
            tv3.heading(column, text=column)
            tv3.column(column, width=50)
        tv3.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame3)
        treescroll.configure(command=tv3.yview)
        tv3.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")
        
        total_label = tk.Label(self, text="Purchase Order: 0")
        total_label.place(rely=0.8, relx=0.03)

        def Load_data():
            file_path3 = "Purchase order.xlsx"
            df = pd.read_excel(file_path3)  # Assuming the file has the required columns
                
                # Convert the DataFrame to a list of lists (as expected by Treeview)
            purchaseOrderlist = df.values.tolist()
            
            
            for row in purchaseOrderlist:
                tv3.insert("", "end", values=row)
            total_label.config(text=f"Total Purchase Order: {len(purchaseOrderlist)}")
            
        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it.
            tv3.delete(*tv3.get_children())  # *=splat operator
            Load_data()

        Load_data()
        
        def open_popup():
            # Create a new popup window
            popup = tk.Toplevel(self)
            popup.title("Add New Purchase Order")  # Set the window title
            popup.geometry("600x500")  # Set the size of the popup window

            # Labels and entry fields for product name, type, and sale price
            tk.Label(popup, text="PO number").pack(pady=5)  # Label for product name
            POnumber_entry = tk.Entry(popup)  # Entry field for product name
            POnumber_entry.pack(pady=5)

            tk.Label(popup, text="Creation date").pack(pady=5)  # Label for product type
            CreateDate_entry = tk.Entry(popup)  # Entry field for product type
            CreateDate_entry.pack(pady=5)

            tk.Label(popup, text="Vendor name").pack(pady=5)  # Label for sale price
            VendorName_entry = tk.Entry(popup)  # Entry field for sale price
            VendorName_entry.pack(pady=5)
            
            tk.Label(popup, text="Buyer").pack(pady=5)  # Label for sale price
            Buyer_entry = tk.Entry(popup)  # Entry field for sale price
            Buyer_entry.pack(pady=5)
            
            tk.Label(popup, text="Total").pack(pady=5)  # Label for sale price
            Total_entry = tk.Entry(popup)  # Entry field for sale price
            Total_entry.pack(pady=5)
            
            # Function to save the new product to the Excel file
            def save_PO():
                # Get the data entered by the user
                new_PO = [
                    POnumber_entry.get(),  # Get the SOnumber
                    CreateDate_entry.get(),  # Get the creation date
                    VendorName_entry.get(),  # Get the customer name
                    Buyer_entry.get(),  # Get the sale person
                    Total_entry.get(),  # Get the totoal amount of sale order
                ]

                # Validate if all fields are filled
                if not all(new_PO):
                    messagebox.showerror("Error", "All fields must be filled")  # Show error if fields are empty
                    return

                try:
                    # Read the existing Excel data into a pandas DataFrame
                    df = pd.read_excel(self.file_path3)

                    # Append the new product to the DataFrame
                    df.loc[len(df)] = new_PO

                    # Save the updated DataFrame back to the Excel file
                    df.to_excel(self.file_path3, index=False)

                    # Refresh the Treeview to show the newly added product
                    Refresh_data()

                    # Close the popup window after saving the product
                    popup.destroy()

                except Exception as e:
                    # Show error message if saving fails
                    messagebox.showerror("Error", f"Failed to save Sale Order: {e}")

            # Save button in the popup window
            tk.Button(popup, text="Save", command=save_PO).pack(pady=20)  # Button to trigger save action

        # Button to open the popup for adding a new product
        add_PO_button = tk.Button(self, text="Add New Sale Order", command=open_popup,  bg=bg3_color, fg=fg3_color, font=("Helvetica", 12, "bold"))
        add_PO_button.place(rely=0.9, relx=0.03)  # Position the button at the bottom of the window

class Person(object):
    # __init__ is known as the constructor
    def __init__(self, name, phone, email, saleperson, city):
        self.name = name
        self.phone = phone
        self.email = email
        self.saleperson = saleperson
        self.city = city
        
class Customer(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.file_path2 = "Customer.xlsx"  # Set self.file_path here
        
        bg2_color = "#FFD700"  # Gold (Yellow) background
        fg2_color = "#000000"  # Black text
        btn2_color = "#FFC300"  # Light yellow for buttons
  
        # Set the background color of the main window
        self.configure(bg=bg2_color)
        
        frame4 = tk.LabelFrame(self, frame_styles, text="Customer", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame4.place(rely=0.05, relx=0.02, height=550, width=1000)
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
        
        total_label = tk.Label(self, text="Customer: 0")
        total_label.place(rely=0.8, relx=0.03)

        def Load_data():
              # Read the data from the Excel file
            file_path2 = "Customer.xlsx"
            df = pd.read_excel(file_path2)  # Assuming the file has the required columns
                
                # Convert the DataFrame to a list of lists (as expected by Treeview)
            customer = df.values.tolist()
            
            for row in customer:
                tv4.insert("", "end", values=row)
            total_label.config(text=f"Total customer: {len(customer)}")
            
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
                    new_person.name,  # Get the product name
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
        add_product_button = tk.Button(self, text="Add New Customer", command=open_popup,  bg=bg2_color, fg=fg2_color, font=("Helvetica", 12, "bold"))
        add_product_button.place(rely=0.9, relx=0.03)  # Position the button at the bottom of the window



class AItool(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="AI tool")
        label1.pack(side="top")
        

class OpenNewWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.title("Here is the Title of the Window")
        self.geometry("500x500")
        self.resizable(0, 0)

        frame1 = ttk.LabelFrame(main_frame, text="This is a ttk LabelFrame")
        frame1.pack(expand=True, fill="both")

        label1 = tk.Label(frame1, font=("Verdana", 20), text="OpenNewWindow Page")
        label1.pack(side="top")


top = LoginPage()
top.title("Shop management - Login Page")
root = MyApp()
root.withdraw()
root.title("Shop management")

root.mainloop()
