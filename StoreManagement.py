import json

class Inventory:
    def __init__(self, filename="inventory.json"):
        self.filename = filename
        self.items = self.load_inventory()

    def load_inventory(self):
        """Load inventory data from a JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_inventory(self):
        """Save the current inventory to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.items, file, indent=4)

    def add_item(self, name, price, quantity):
        """Add a new item or update an existing one."""
        if name in self.items:
            self.items[name]['quantity'] += quantity
        else:
            self.items[name] = {'price': price, 'quantity': quantity}
        self.save_inventory()
        print(f"Added {quantity} of {name} at ${price} each.")

    def remove_item(self, name):
        """Remove an item from inventory."""
        if name in self.items:
            del self.items[name]
            self.save_inventory()
            print(f"Removed {name} from inventory.")
        else:
            print("Error: Item not found.")

    def display_inventory(self):
        """Display the current inventory."""
        if not self.items:
            print("Inventory is empty.")
        else:
            print("\nCurrent Inventory:")
            for name, details in self.items.items():
                print(f"{name}: ${details['price']} - {details['quantity']} in stock")

    def search_item(self, name):
        """Search for an item and display its details."""
        if name in self.items:
            details = self.items[name]
            print(f"\n{name}: ${details['price']} - {details['quantity']} in stock")
        else:
            print("Item not found.")


def main():
    inventory = Inventory()

    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Display Inventory")
        print("4. Search Item")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter item name: ")
            try:
                price = float(input("Enter item price: "))
                quantity = int(input("Enter quantity: "))
                inventory.add_item(name, price, quantity)
            except ValueError:
                print("Invalid input. Please enter valid price and quantity.")
        elif choice == '2':
            name = input("Enter item name to remove: ")
            inventory.remove_item(name)
        elif choice == '3':
            inventory.display_inventory()
        elif choice == '4':
            name = input("Enter item name to search: ")
            inventory.search_item(name)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
