import json
import datetime

class OrderManagementSystem:
    def __init__(self, inventory_file="inventory.json", orders_file="orders.json"):
        self.inventory_file = inventory_file
        self.orders_file = orders_file
        self.inventory = self.load_data(self.inventory_file)
        self.orders = self.load_data(self.orders_file)

    def load_data(self, filename):
        """Load data from a JSON file."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if "inventory" in filename else []

    def save_data(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def place_order(self, customer_name, items):
        """Create a new order and update inventory."""
        order_id = len(self.orders) + 1
        total_price = 0
        for barcode, quantity in items.items():
            if barcode in self.inventory and self.inventory[barcode]['quantity'] >= quantity:
                self.inventory[barcode]['quantity'] -= quantity
                total_price += self.inventory[barcode]['price'] * quantity
            else:
                print(f"Error: Insufficient stock for {barcode}.")
                return

        order = {
            "order_id": order_id,
            "customer": customer_name,
            "items": items,
            "total_price": total_price,
            "status": "Processing",
            "date": str(datetime.datetime.now())
        }
        self.orders.append(order)
        self.save_data(self.orders_file, self.orders)
        self.save_data(self.inventory_file, self.inventory)
        print(f"Order {order_id} placed successfully!")

    def update_order_status(self, order_id, status):
        """Update the status of an existing order."""
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = status
                self.save_data(self.orders_file, self.orders)
                print(f"Order {order_id} status updated to {status}.")
                return
        print("Order not found.")

    def track_order(self, order_id):
        """Retrieve and display order details."""
        for order in self.orders:
            if order["order_id"] == order_id:
                print("Order Details:", json.dumps(order, indent=4))
                return
        print("Order not found.")

    def run(self):
        """Main function to handle order management interactions."""
        while True:
            action = input("Choose an action: place, update, track, or quit: ")
            if action == "quit":
                break
            elif action == "place":
                customer_name = input("Enter customer name: ")
                items = {}
                while True:
                    barcode = input("Enter barcode (or 'done' to finish): ")
                    if barcode.lower() == "done":
                        break
                    quantity = int(input("Enter quantity: "))
                    items[barcode] = quantity
                self.place_order(customer_name, items)
            elif action == "update":
                order_id = int(input("Enter order ID: "))
                status = input("Enter new status: ")
                self.update_order_status(order_id, status)
            elif action == "track":
                order_id = int(input("Enter order ID: "))
                self.track_order(order_id)
            else:
                print("Invalid action.")

if __name__ == "__main__":
    oms = OrderManagementSystem()
    oms.run()
