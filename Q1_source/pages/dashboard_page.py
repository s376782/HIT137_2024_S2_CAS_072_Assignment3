#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from services.purchase_order_service import PurchaseOrderService
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """
    DashboardPage extends BasePage and visualizes sales, purchases, and product data
    using bar and pie charts.
    """

    @staticmethod
    def __create_barchart(x, y,
                          screen_height, screen_width,
                          labelx="Customer", labely="Total amount",
                          colors='maroon',
                          titleofchart="Total order value for each customer",
                          rotation=45):
        
        """(private) Creates a bar chart and returns the figure."""
        fig, ax = plt.subplots(figsize= (int(screen_width/210), int(screen_height/220)))
        ax.bar(x, y, color=colors, width=0.4)
        ax.set_xlabel(labelx)
        ax.set_ylabel(labely)
        ax.set_title(titleofchart, fontweight = "bold", fontsize = "16")

        ax.set_xticks(range(len(x)))  # Set positions for each bar
        ax.set_xticklabels(x, rotation=rotation)

        plt.tight_layout()
        return fig

    @staticmethod
    def __create_piechart(labels, values,
                          screen_width, screen_height,
                          title="Distribution of Types"):
        """(private) Creates a pie chart and returns the figure."""
        fig, ax = plt.subplots(figsize=(int(screen_height/210), int(screen_width/220)))
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title(title, fontweight = "bold", fontsize = "16")
        plt.tight_layout()
        return fig

    def __init__(self, parent, controller,
                 sale_order_service: SaleOrderService,
                 purchase_order_service: PurchaseOrderService,
                 product_service: ProductService):
        """
        Initializes the dashboard page and displays charts for sales and products.

        Args:
            parent: The parent widget.
            controller: Manages page transitions.
            sale_order_service (SaleOrderService): Service for fetching sales data.
            purchase_order_service (PurchaseOrderService): Service for fetching purchase data.
            product_service (ProductService): Service for fetching product data.
        """
        super().__init__(parent, controller)

        # Colors for UI elements
        bg2_color = "#8B0000"  # Dark red for background
        fg2_color = "#ffffff"  # White text remains unchanged

        # Set the background color of the main window
        self.configure(bg=bg2_color)

        frame_dashboard = tk.LabelFrame(self, text="Dashboard",
                                         bg=bg2_color, fg=fg2_color,
                                         font=("Helvetica", 16, "bold"))
        frame_dashboard.place(rely=0, relx=0, height=self._screen_height, width=self._screen_width)

        # Fetch data for charts
        customers, customer_totals = sale_order_service.get_top_customers()
        sales_persons, sales_totals = sale_order_service.get_top_sale_persons()
        vendors, vendor_totals = purchase_order_service.get_top_venders()
        labels, counts = product_service.get_type_report()

        # Customer order bar chart
        self.__add_chart(frame_dashboard, row=0, column=0, 
                         figure=DashboardPage.__create_barchart(customers, customer_totals,
                                                                self._screen_height, self._screen_width,
                                                                "Customer", "Total sale amount", 
                                                                'maroon', "Total order value for top 10 customers"))

        # Sale person bar chart
        self.__add_chart(frame_dashboard, row=0, column=1, 
                         figure=DashboardPage.__create_barchart(sales_persons, sales_totals,
                                                                self._screen_height, self._screen_width,
                                                                "Sale person", "Total sale amount", 
                                                                'blue', "Total sale amount for top 10 sellers"))

        # Vendor bar chart
        self.__add_chart(frame_dashboard, row=1, column=0, 
                         figure=DashboardPage.__create_barchart(vendors, vendor_totals,
                                                                self._screen_height, self._screen_width, 
                                                               "Vendor name", "Total purchase amount", 
                                                               'yellow', "Total purchase amount for top 10 vendors"))

        # Product type pie chart
        self.__add_chart(frame_dashboard, row=1, column=1, 
                         figure=DashboardPage.__create_piechart(labels, counts,
                                                                self._screen_height, self._screen_width,                                                          
                                                                title="Distribution of Product Types"))

        # Run the Tkinter main loop
        label1 = tk.Label(self._main_frame, font=("Verdana", 20), text="AI tool")
        label1.pack(side="top")

    def __add_chart(self, parent, row, column, figure):
        """(private) Helper method to add a chart to the specified frame."""
        frame = tk.Frame(parent)
        frame.grid(row=row, column=column, padx=10, pady=5)
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


