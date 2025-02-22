import json

class CRMSystem:
    def __init__(self, filename="customers.json"):
        self.filename = filename
        self.customers = self.load_customers()

    def load_customers(self):
        """Load customer data from a JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_customers(self):
        """Save the current customer data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.customers, file, indent=4)

    def add_customer(self, name, contact_info):
        """Add a new customer profile."""
        if name in self.customers:
            print("Customer already exists.")
            return
        self.customers[name] = {
            "contact_info": contact_info,
            "purchase_history": [],
            "loyalty_points": 0
        }
        self.save_customers()
        print(f"Customer {name} added successfully.")

    def remove_customer(self, name):
        """Remove a customer profile."""
        if name in self.customers:
            del self.customers[name]
            self.save_customers()
            print(f"Customer {name} removed successfully.")
        else:
            print("Error: Customer not found.")

    def record_purchase(self, name, item, amount):
        """Record a customer's purchase."""
        if name in self.customers:
            self.customers[name]["purchase_history"].append({"item": item, "amount": amount})
            self.customers[name]["loyalty_points"] += int(amount / 10)  # Example: 1 point per $10 spent
            self.save_customers()
            print(f"Purchase recorded for {name}.")
        else:
            print("Error: Customer not found.")

    def display_customer(self, name):
        """Display a customer's details."""
        if name in self.customers:
            customer = self.customers[name]
            print(f"\nCustomer: {name}")
            print(f"Contact Info: {customer['contact_info']}")
            print(f"Loyalty Points: {customer['loyalty_points']}")
            print("Purchase History:")
            for purchase in customer["purchase_history"]:
                print(f" - {purchase['item']}: ${purchase['amount']}")
        else:
            print("Customer not found.")


def main():
    crm = CRMSystem()

    while True:
        print("\nCustomer Relationship Management System")
        print("1. Add Customer")
        print("2. Remove Customer")
        print("3. Record Purchase")
        print("4. Display Customer")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter customer name: ")
            contact_info = input("Enter contact information: ")
            crm.add_customer(name, contact_info)
        elif choice == '2':
            name = input("Enter customer name to remove: ")
            crm.remove_customer(name)
        elif choice == '3':
            name = input("Enter customer name: ")
            item = input("Enter item purchased: ")
            try:
                amount = float(input("Enter amount spent: "))
                crm.record_purchase(name, item, amount)
            except ValueError:
                print("Invalid input. Please enter a valid amount.")
        elif choice == '4':
            name = input("Enter customer name: ")
            crm.display_customer(name)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()