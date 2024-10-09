import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import openpyxl as op
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

#Add new object button
bg0_color = "#7B68EE"  # Medium Slate Blue (stronger purple)
fg0_color = "#FFFFFF"  # White text
btn0_color = "#6A5ACD"  # Slate Blue for buttons (also stronger)



class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        self.geometry("626x500")  # Sets window size to 626w x 431h pixels
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
    
        menu_dashboard = tk.Menu(self, tearoff=0)
        self.add_cascade(label="DASHBOARD", menu=menu_dashboard)
        menu_dashboard.add_command(label="DASHBOARD", command=lambda: parent.show_frame(Dashboard), font=bold_font)

        menu_sale = tk.Menu(self, tearoff=0)
        self.add_cascade(label="SALE", menu=menu_sale)
        menu_sale.add_command(label="SALE ORDER", command=lambda: parent.show_frame(SaleOrder), font=bold_font)

        menu_purchase = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PURCHASE", menu=menu_purchase)
        menu_purchase.add_command(label="PURCHASE ORDER", command=lambda: parent.show_frame(PurchaseOrder), font=bold_font)
        
        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="PRODUCT", menu=menu_file)
        menu_file.add_command(label="LIST OF PRODUCT", command=lambda: parent.show_frame(Productlist), font=bold_font)


        menu_contact = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CONTACT", menu=menu_contact)
        menu_contact.add_command(label="LIST OF CUSTOMER", command=lambda: parent.show_frame(Customer), font=bold_font)



class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#FFF0F5", height=800, width=1900)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        pages = (Dashboard, SaleOrder, PurchaseOrder,Productlist, Customer)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Dashboard)
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def Quit_application(self):
        self.destroy()


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
  # Get screen width and height
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Set the main_frame to fill the screen
        self.main_frame = tk.Frame(self, bg="#FFFFFF", height=screen_height, width=screen_width)
        self.main_frame.pack(fill="both", expand=True)  # Ensure it expands to fill the entire screen
        
        
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
class baseobject(object):
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name


class SO(baseobject):
    # __init__ is known as the constructor
    def __init__(self, name, date, cusname, saleperson, total):
        super().__init__(name)
        self.date = date
        self.cusname = cusname
        self.saleperson = saleperson
        self.total = total
        
    def get_name(self):
        return "SO" + str(super().get_name())
    
    
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
            file_path2 = "Sale Order.xlsx"
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

class PO(baseobject):
    # __init__ is known as the constructor
    def __init__(self, name, date, vendor, buyer, total):
        super().__init__(name)
        self.date = date
        self.vendor = vendor
        self.buyer = buyer
        self.total = total
    def get_name(self):
        return "PO" + str(super().get_name())
    
    
class PurchaseOrder(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
                # Define the path to the Excel file as an instance variable
        self.file_path3 = "Purchase order.xlsx"  # Set self.file_path here

        # Define colors
        bg3_color = "#3CB371"  # Medium sea green for background
        fg3_color = "#ffffff"  # White text remains unchanged
        btn3_color = "#32CD32"  # Lime green for buttons

        # Set the background color of the main window
        self.configure(bg=bg3_color)
        frame3 = tk.LabelFrame(self, text="Purchase Orders", bg=bg3_color, fg=fg3_color, font=("Helvetica", 16, "bold"))
        frame3.place(rely=0, relx=0, height=700, width=1900)
        
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
        
        total_label = tk.Label(self, text="SUMMARY", bg="#FFFFFF", fg = "#000000", font=("Arial", 12, "bold") )
        total_label.place(rely=0.66, relx=0.02)
        
        total_label1 = tk.Label(self, text="Total Purchase Order: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 9, "bold"))
        total_label.place(rely=0.7, relx=0.02)
        
        #Count data total
        total_label2 = tk.Label(self, text="Total amount: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        total_label2.place(rely=0.74, relx=0.02)
        
        #Count Total vendor
        total_label3 = tk.Label(self, text="Total customer have orders: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        total_label3.place(rely=0.78, relx=0.02)
        
        #Count Top 1 regular vendor
        total_label4 = tk.Label(self, text="Top regular vendor: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        total_label4.place(rely=0.82, relx=0.02)
        
        #Count Top buyer
        total_label5 = tk.Label(self, text="Top buyer: 0", bg="#FFFFFF", fg = "#3CB371", font=("Arial", 11, "bold"))
        total_label5.place(rely=0.86, relx=0.02)        


        def Load_data():
            file_path3 = "Purchase order.xlsx"
            df = pd.read_excel(file_path3)  # Assuming the file has the required columns
                
                # Convert the DataFrame to a list of lists (as expected by Treeview)
            purchaseOrderlist = df.values.tolist()
            
            
            for row in purchaseOrderlist:
                tv3.insert("", "end", values=row)
            # total
            #Count number of PO
            total_label1.config(text=f"- Total Purchase Order: {len(purchaseOrderlist)}")
            
            #Count total amount
            total_label2.config(text=f"- Total amount: {df["Total"].sum()}")
            
            #Get number of customers have orders
            total_label3.config(text=f"- Total customer have orders: {df["Vendor name"].nunique()}")
            
            #Get Top 1 regular customer
            top_vendor = df.groupby('Vendor name')['Total'].sum().idxmax()  #find sale person
            max_amount = df.groupby('Vendor name')['Total'].sum().max()  # Lấy tổng doanh số của người đó
            total_label4.config(text=f"- Top vendor: {top_vendor} with amount: {max_amount}")
            
            #Get Top 1 buyer
            top_buyer = df.groupby('Buyer')['Total'].sum().idxmax()  #find sale person
            max_buying_amount = df.groupby('Buyer')['Total'].sum().max()  # Lấy tổng doanh số của người đó
            total_label5.config(text=f"- Top Sales person: {top_buyer} with sales amount: {max_buying_amount}")
               
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
                PurchaseOrder = PO(POnumber_entry.get(), CreateDate_entry.get(), VendorName_entry.get(), Buyer_entry.get(), Total_entry.get())
                # Get the data entered by the user
                new_PO = [
                    PurchaseOrder.get_name(),  # Get the SOnumber
                    PurchaseOrder.date,  # Get the SOnumber
                    PurchaseOrder.vendor,  # Get the SOnumber
                    PurchaseOrder.buyer,  # Get the SOnumber
                    PurchaseOrder.total,  # Get the SOnumber
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
        add_PO_button = tk.Button(self, text="Add new purchase order", command=open_popup,  bg=bg0_color, fg=fg0_color, font=("Helvetica", 10, "bold"))
        add_PO_button.place(rely=0, relx=0.85)  # Position the button at the bottom of the window



class Product(baseobject):
    # __init__ is known as the constructor
    def __init__(self, name, type, saleprice):
        super().__init__(name)
        self.type = type
        self.saleprice = saleprice


class Productlist(GUI):  # inherits from the GUI class
    
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        # Define the path to the Excel file as an instance variable
        self.file_path = "Product.xlsx"  # Set self.file_path here

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
            file_path = "Product.xlsx"
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

class Person(baseobject):
    # __init__ is known as the constructor
    def __init__(self, name, phone, email, saleperson, city):
        super().__init__(name)
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
            file_path2 = "Customer.xlsx"
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



class Dashboard(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged
        btn2_color = "#A52A2A"  # Brownish red for buttons

        # Set the background color of the main window
        self.configure(bg=bg2_color)
        
        frame5 = tk.LabelFrame(self, text="Dashboard", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame5.place(rely=0, relx=0, height=1200, width=1900)
        
        # Read the existing Excel data into a pandas DataFrame
        df1 = pd.read_excel("Sale Order.xlsx")
        df2 = pd.read_excel("Purchase order.xlsx")
        df3 = pd.read_excel("Product.xlsx")
        df4 = pd.read_excel("Customer.xlsx")

    # # Get unique customer names and grouped totals
    #     X1 = df1['Customer name'].unique()
    #     Y1 = df1.groupby('Customer name')['Total'].sum()
        # Get top 10 customer names and grouped totals
        top_customers = df1.groupby('Customer name')['Total'].sum().sort_values(ascending=False).head(10)
        X1 = top_customers.index  # Customer names
        Y1 = top_customers.values  # Corresponding totals

        # Get unique sale person names and grouped totals
        top_saleperson = df1.groupby('Sale person')['Total'].sum().sort_values(ascending=False).head(10)
        X2 = top_saleperson.index
        Y2 = top_saleperson.values
        #Y2 = Y2pre.sort_values(ascending=False).head(5)
        
        
        # Get unique vendor names and grouped totals
        top_vendor = df2.groupby('Vendor name')['Total'].sum().sort_values(ascending=False).head(10)
        X3 = top_vendor.index
        Y3 = top_vendor.values
    

        # Function to create bar charts and return figure
        def create_barchart(x, y, labelx="Customer", labely="Total amount", colors='maroon', titleofchart="Total order value for each customer", rotation=45):
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(x, y, color=colors, width=0.4)
            ax.set_xlabel(labelx)
            ax.set_ylabel(labely)
            ax.set_title(titleofchart, fontweight = "bold", fontsize = "16")
            ax.set_xticklabels(x, rotation=rotation)
            plt.tight_layout() 
            return fig

        # Function to create pie chart and return figure
        def create_piechart(labels, values, title="Distribution of Types"):
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title(title, fontweight = "bold", fontsize = "16")
            plt.tight_layout()
            return fig

        # Frame for Customer Order Bar Chart
        framebar1 = tk.Frame(frame5)
        framebar1.grid(row=0, column=0, padx=10, pady=10)

        # Customer order bar chart
        # Sort and get the top 5 customers
        
        fig1 = create_barchart(X1, Y1, "Customer", "Total sale amount", 'maroon', "Total order value for top 10 customers")
        canvas1 = FigureCanvasTkAgg(fig1, master=framebar1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Frame for Sale Person Bar Chart
        framebar2 = tk.Frame(frame5)
        framebar2.grid(row=0, column=1, padx=10, pady=10)

        # Sale person bar chart
        fig2 = create_barchart(X2, Y2, "Sale person", "Total sale amount", 'blue', "Total sale amount for top 10 sellers")
        canvas2 = FigureCanvasTkAgg(fig2, master=framebar2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

        # Frame for Vendor Bar Chart
        framebar3 = tk.Frame(frame5)
        framebar3.grid(row=1, column=0, padx=10, pady=10)

        # Vendor bar chart
        fig3 = create_barchart(X3, Y3, "Vendor name", "Total purchase amount", 'yellow', "Total purchase amount for top 10 vendors")
        canvas3 = FigureCanvasTkAgg(fig3, master=framebar3)
        canvas3.draw()
        canvas3.get_tk_widget().pack()

        # Frame for Pie Chart (Types)
        framebar5 = tk.Frame(frame5)
        framebar5.grid(row=1, column=1, padx=10, pady=10)

        # Pie chart for good types
        mylabel = df3["Type"].unique()
        Y5 = df3.groupby("Type")["Name"].count()

        fig5 = create_piechart(mylabel, Y5, title="Distribution of Product Types")
        canvas5 = FigureCanvasTkAgg(fig5, master=framebar5)
        canvas5.draw()
        canvas5.get_tk_widget().pack()

        # Run the Tkinter main loop
        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="AI tool")
        label1.pack(side="top")


top = LoginPage()
top.title("Shop management - Login Page")
root = MyApp()
root.withdraw()
root.title("Shop management")

root.mainloop()
