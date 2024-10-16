import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from application import Application

from services.purchase_order_service import PurchaseOrderService

if __name__ == "__main__":
    app = Application()
    app.run()
