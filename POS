import json
import datetime

class POS:
    def __init__(self, inventory_file="inventory.json", sales_file="sales.json"):
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.inventory = self.load_data(self.inventory_file)
        self.sales = self.load_data(self.sales_file)

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

    def scan_barcode(self, barcode):
        """Retrieve item details by barcode."""
        return self.inventory.get(barcode, None)

    def process_payment(self, total_amount, payment_method):
        """Handle payment processing."""
        if payment_method not in ["cash", "credit card"]:
            print("Invalid payment method.")
            return False
        print(f"Payment of ${total_amount:.2f} processed via {payment_method}.")
        return True

    def generate_receipt(self, cart, total_amount, payment_method):
        """Generate a receipt for the transaction."""
        receipt = {
            "date": str(datetime.datetime.now()),
            "items": cart,
            "total": total_amount,
            "payment_method": payment_method
        }
        self.sales.append(receipt)
        self.save_data(self.sales_file, self.sales)
        print("Receipt Generated:", json.dumps(receipt, indent=4))

    def update_inventory(self, cart):
        """Update inventory based on the purchased items."""
        for barcode, quantity in cart.items():
            if barcode in self.inventory and self.inventory[barcode]['quantity'] >= quantity:
                self.inventory[barcode]['quantity'] -= quantity
            else:
                print(f"Error: Insufficient stock for {barcode}.")
        self.save_data(self.inventory_file, self.inventory)

    def run(self):
        """Main function to handle POS transactions."""
        cart = {}
        while True:
            barcode = input("Scan barcode (or type 'done' to finish): ")
            if barcode.lower() == 'done':
                break
            item = self.scan_barcode(barcode)
            if item:
                quantity = int(input(f"Enter quantity for {item['name']}: "))
                cart[barcode] = quantity
            else:
                print("Item not found.")

        total_amount = sum(self.inventory[b]['price'] * q for b, q in cart.items())
        print(f"Total amount: ${total_amount:.2f}")
        payment_method = input("Enter payment method (cash/credit card): ")
        if self.process_payment(total_amount, payment_method):
            self.generate_receipt(cart, total_amount, payment_method)
            self.update_inventory(cart)

if __name__ == "__main__":
    pos_system = POS()
    pos_system.run()