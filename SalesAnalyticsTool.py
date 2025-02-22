import json
import matplotlib.pyplot as plt
from collections import Counter

class SalesAnalytics:
    def __init__(self, sales_file="sales.json", inventory_file="inventory.json"):
        self.sales_file = sales_file
        self.inventory_file = inventory_file
        self.sales = self.load_data(self.sales_file)
        self.inventory = self.load_data(self.inventory_file)

    def load_data(self, filename):
        """Load data from a JSON file."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] if "sales" in filename else {}

    def save_data(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def record_sale(self, product, quantity, price):
        """Record a new sale and update inventory."""
        if product in self.inventory and self.inventory[product]['quantity'] >= quantity:
            self.sales.append({"product": product, "quantity": quantity, "price": price})
            self.inventory[product]['quantity'] -= quantity
            self.save_data(self.sales_file, self.sales)
            self.save_data(self.inventory_file, self.inventory)
            print(f"Sale recorded: {quantity} x {product} at ${price} each.")
        else:
            print("Error: Insufficient stock or product not found.")

    def generate_sales_report(self):
        """Generate a sales report including total revenue and best-selling products."""
        if not self.sales:
            print("No sales data available.")
            return

        total_revenue = sum(sale['quantity'] * sale['price'] for sale in self.sales)
        product_counts = Counter(sale['product'] for sale in self.sales)
        best_selling = product_counts.most_common(1)[0] if product_counts else (None, 0)

        print("\nSales Report:")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Best-Selling Product: {best_selling[0]} (Sold {best_selling[1]} times)")

    def visualize_sales(self):
        """Generate a bar chart visualization of sales data."""
        if not self.sales:
            print("No sales data to visualize.")
            return

        product_counts = Counter(sale['product'] for sale in self.sales)
        products, quantities = zip(*product_counts.items())

        plt.bar(products, quantities, color='blue')
        plt.xlabel("Products")
        plt.ylabel("Quantity Sold")
        plt.title("Sales Data Visualization")
        plt.xticks(rotation=45)
        plt.show()

    def inventory_turnover_report(self):
        """Analyze inventory turnover and stock levels."""
        print("\nInventory Turnover Report:")
        for product, details in self.inventory.items():
            print(f"{product}: {details['quantity']} remaining in stock")


def main():
    analytics = SalesAnalytics()

    while True:
        print("\nSales Analytics and Reporting Tool")
        print("1. Record Sale")
        print("2. Generate Sales Report")
        print("3. Visualize Sales Data")
        print("4. Inventory Turnover Report")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            product = input("Enter product name: ")
            try:
                quantity = int(input("Enter quantity sold: "))
                price = float(input("Enter price per unit: "))
                analytics.record_sale(product, quantity, price)
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and price.")
        elif choice == '2':
            analytics.generate_sales_report()
        elif choice == '3':
            analytics.visualize_sales()
        elif choice == '4':
            analytics.inventory_turnover_report()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()