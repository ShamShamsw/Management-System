import json
import datetime

class SupplyChainManagementSystem:
    def __init__(self, inventory_file="inventory.json", shipments_file="shipments.json", orders_file="orders.json"):
        self.inventory_file = inventory_file
        self.shipments_file = shipments_file
        self.orders_file = orders_file
        self.inventory = self.load_data(self.inventory_file)
        self.shipments = self.load_data(self.shipments_file)
        self.orders = self.load_data(self.orders_file)

    def load_data(self, filename):
        """Load data from a JSON file."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def track_shipment(self, tracking_id):
        """Retrieve and display shipment details."""
        for shipment in self.shipments:
            if shipment["tracking_id"] == tracking_id:
                print("Shipment Details:", json.dumps(shipment, indent=4))
                return
        print("Shipment not found.")

    def reorder_alerts(self):
        """Check inventory levels and generate reorder alerts."""
        alerts = []
        for item, details in self.inventory.items():
            if details['quantity'] <= details['reorder_level']:
                alerts.append(f"Reorder needed for {item}, current stock: {details['quantity']}")
        if alerts:
            print("Reorder Alerts:")
            for alert in alerts:
                print(alert)
        else:
            print("All inventory levels are sufficient.")

    def add_shipment(self, tracking_id, supplier, items, estimated_arrival):
        """Add a new shipment record."""
        shipment = {
            "tracking_id": tracking_id,
            "supplier": supplier,
            "items": items,
            "estimated_arrival": estimated_arrival,
            "status": "In Transit"
        }
        self.shipments.append(shipment)
        self.save_data(self.shipments_file, self.shipments)
        print(f"Shipment {tracking_id} added successfully!")

    def update_inventory(self, tracking_id):
        """Update inventory based on received shipment."""
        for shipment in self.shipments:
            if shipment["tracking_id"] == tracking_id and shipment["status"] == "In Transit":
                for item, quantity in shipment["items"].items():
                    if item in self.inventory:
                        self.inventory[item]["quantity"] += quantity
                    else:
                        self.inventory[item] = {"quantity": quantity, "reorder_level": 10}
                shipment["status"] = "Received"
                self.save_data(self.inventory_file, self.inventory)
                self.save_data(self.shipments_file, self.shipments)
                print(f"Inventory updated for shipment {tracking_id}.")
                return
        print("Shipment not found or already received.")

    def run(self):
        """Main function to handle supply chain interactions."""
        while True:
            action = input("Choose an action: track_shipment, reorder_alerts, add_shipment, update_inventory, or quit: ")
            if action == "quit":
                break
            elif action == "track_shipment":
                tracking_id = input("Enter tracking ID: ")
                self.track_shipment(tracking_id)
            elif action == "reorder_alerts":
                self.reorder_alerts()
            elif action == "add_shipment":
                tracking_id = input("Enter tracking ID: ")
                supplier = input("Enter supplier name: ")
                items = {}
                while True:
                    item = input("Enter item name (or 'done' to finish): ")
                    if item.lower() == "done":
                        break
                    quantity = int(input("Enter quantity: "))
                    items[item] = quantity
                estimated_arrival = input("Enter estimated arrival date (YYYY-MM-DD): ")
                self.add_shipment(tracking_id, supplier, items, estimated_arrival)
            elif action == "update_inventory":
                tracking_id = input("Enter tracking ID of received shipment: ")
                self.update_inventory(tracking_id)
            else:
                print("Invalid action.")

if __name__ == "__main__":
    scms = SupplyChainManagementSystem()
    scms.run()