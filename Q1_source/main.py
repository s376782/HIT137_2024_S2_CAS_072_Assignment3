import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from services.product_service import ProductService
from services.sale_order_service import SaleOrderService
from application import MainWindow

from services.purchase_order_service import PurchaseOrderService

if __name__ == "__main__":
    product_service = ProductService()
    purchase_order_service = PurchaseOrderService()
    sale_order_service = SaleOrderService()
    app = MainWindow(product_service, purchase_order_service, sale_order_service)
    app.mainloop()