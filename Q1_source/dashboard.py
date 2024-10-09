# import pandas as pd
# import matplotlib.pyplot as plt

# # Read the existing Excel data into a pandas DataFrame
# df1 = pd.read_excel("Sale Order.xlsx")
# df2 = pd.read_excel("Purchase order.xlsx")    
# df3 = pd.read_excel("Product.xlsx")
# df4 = pd.read_excel("Customer.xlsx")


# # Get unique customer names
# X1 = df1['Customer name'].unique()
# Y1 = df1.groupby('Customer name')['Total'].sum()


# # barchart for sale person
# X2 = df1['Sale person'].unique()
# Y2 = df1.groupby('Sale person')['Total'].sum()

# # barchart for vendor
# X3 = df2['Vendor name'].unique()
# Y3 = df2.groupby('Vendor name')['Total'].sum()

# # barchart for buyer
# X4 = df2['Buyer'].unique()
# Y4 = df2.groupby('Buyer')['Total'].sum()


# def barchart(x, y, labelx = "Customer" , labely = "Total amount", colors = 'maroon', titleofchart = "Total order value for each customer"):
#         fig = plt.figure(figsize=(10, 5))
#         plt.bar(x, y, color=colors, width=0.4)
#         plt.xlabel(labelx)
#         plt.ylabel(labely)
#         plt.title(titleofchart)
#         plt.xticks(rotation=45)  # Rotate customer names if necessary
#         plt.tight_layout()  # Ensure layout doesn't cut off labels
#         plt.show()

# barchart(X1, Y1, "Customer", "Total sale amount", 'maroon',"Total order value for each customer")
# barchart(X2, Y2, "Sale person", "Total sale amount", 'blue',"Total sale amount for each sale person")
# barchart(X3, Y3, "Vendor name", "Total purchase amount", 'yellow',"Total purchase amount for each vendor")
# barchart(X4, Y4, "Buyer", "Total purchase amount", 'brown',"Total purchase amount for buyer")


# # Pie chart for good types
# mylabel = df3["Type"].unique()
# Y5 = df3.groupby("Type")["Name"].count()
# # Create the pie chart
# plt.pie(Y5, labels=mylabel, autopct='%1.1f%%')
# # Adjust the legend position using bbox_to_anchor
# plt.legend(loc="best", bbox_to_anchor=(1, 0.5))  # Moves legend to the right with spacing
# # Show the plot
# plt.show()
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Read the existing Excel data into a pandas DataFrame
df1 = pd.read_excel("Sale Order.xlsx")
df2 = pd.read_excel("Purchase order.xlsx")
df3 = pd.read_excel("Product.xlsx")
df4 = pd.read_excel("Customer.xlsx")

# Get unique customer names and grouped totals
X1 = df1['Customer name'].unique()
Y1 = df1.groupby('Customer name')['Total'].sum()

# Get unique sale person names and grouped totals
X2 = df1['Sale person'].unique()
Y2 = df1.groupby('Sale person')['Total'].sum()

# Get unique vendor names and grouped totals
X3 = df2['Vendor name'].unique()
Y3 = df2.groupby('Vendor name')['Total'].sum()

# Get unique buyer names and grouped totals
X4 = df2['Buyer'].unique()
Y4 = df2.groupby('Buyer')['Total'].sum()

# Function to create bar charts and return figure
def create_barchart(x, y, labelx="Customer", labely="Total amount", colors='maroon', titleofchart="Total order value for each customer", rotation=45):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(x, y, color=colors, width=0.4)
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    ax.set_title(titleofchart)
    ax.set_xticklabels(x, rotation=rotation)
    return fig

# Function to create pie chart and return figure
def create_piechart(labels, values, title="Distribution of Types"):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title(title)
    return fig

# Tkinter setup
root = tk.Tk()
root.title("Dashboard")

# Create a Tkinter frame for layout management
frame = tk.Frame(root)
frame.pack(padx=0, pady=5)

# Frame for Customer Order Bar Chart
frame1 = tk.Frame(frame)
frame1.grid(row=0, column=0, padx=10, pady=5)

# Customer order bar chart
fig1 = create_barchart(X1, Y1, "Customer", "Total sale amount", 'maroon', "Total order value for each customer")
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()

# Frame for Sale Person Bar Chart
frame2 = tk.Frame(frame)
frame2.grid(row=0, column=1, padx=30, pady=30)

# Sale person bar chart
fig2 = create_barchart(X2, Y2, "Sale person", "Total sale amount", 'blue', "Total sale amount for each sale person")
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.draw()
canvas2.get_tk_widget().pack()

# Frame for Vendor Bar Chart
frame3 = tk.Frame(frame)
frame3.grid(row=1, column=0, padx=30, pady=30)

# Vendor bar chart
fig3 = create_barchart(X3, Y3, "Vendor name", "Total purchase amount", 'yellow', "Total purchase amount for each vendor")
canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
canvas3.draw()
canvas3.get_tk_widget().pack()

# Frame for Buyer Bar Chart
frame4 = tk.Frame(frame)
frame4.grid(row=1, column=1, padx=10, pady=10)

# # Buyer bar chart
fig4 = create_barchart(X4, Y4, "Buyer", "Total purchase amount", 'brown', "Total purchase amount for buyer")
canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
canvas4.draw()
canvas4.get_tk_widget().pack()

# Frame for Pie Chart (Types)
frame5 = tk.Frame(frame)
frame5.grid(row=2, column=0, padx=30, pady=30, columnspan=2)

# Pie chart for good types
mylabel = df3["Type"].unique()
Y5 = df3.groupby("Type")["Name"].count()

fig5 = create_piechart(mylabel, Y5, title="Distribution of Product Types")
canvas5 = FigureCanvasTkAgg(fig5, master=frame5)
canvas5.draw()
canvas5.get_tk_widget().pack()

# Run the Tkinter main loop
root.mainloop()


