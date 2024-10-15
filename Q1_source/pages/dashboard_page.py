import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from services.purchase_order_service import PurchaseOrderService
from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(
            self, parent,
            controller,
            sale_order_service: SaleOrderService,
            purchase_order_service: PurchaseOrderService,
            product_service: ProductService):
        super().__init__(parent, controller)

        # Define the path to the Excel file as an instance variable
        # Define colors
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged
        btn2_color = "#A52A2A"  # Brownish red for buttons

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame5 = tk.LabelFrame(self, text="Dashboard", bg=bg2_color, fg=fg2_color, font=("Helvetica", 16, "bold"))
        frame5.place(rely=0, relx=0, height=1200, width=1900)

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

        # Get top 10 customer names and grouped totals
        (X1, Y1) = sale_order_service.get_top_customers()

        # Get unique sale person names and grouped totals
        (X2, Y2) = sale_order_service.get_top_sale_persons()

        # Get unique vendor names and grouped totals
        (X3, Y3) = purchase_order_service.get_top_venders()

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
        labels, counts = product_service.get_type_report()

        fig5 = create_piechart(labels, counts, title="Distribution of Product Types")
        canvas5 = FigureCanvasTkAgg(fig5, master=framebar5)
        canvas5.draw()
        canvas5.get_tk_widget().pack()

        # Run the Tkinter main loop
        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="AI tool")
        label1.pack(side="top")