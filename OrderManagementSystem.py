import json
import datetime
import random

class ProductRecommendationEngine:
    def __init__(self, inventory_file="inventory.json", orders_file="orders.json", recommendations_file="recommendations.json"):
        self.inventory_file = inventory_file
        self.orders_file = orders_file
        self.recommendations_file = recommendations_file
        self.inventory = self.load_data(self.inventory_file)
        self.orders = self.load_data(self.orders_file)
        self.recommendations = self.load_data(self.recommendations_file)

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

    def generate_recommendations(self):
        """Generate product recommendations based on previous purchases."""
        product_pairs = {}
        for order in self.orders:
            items = list(order["items"].keys())
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    pair = tuple(sorted([items[i], items[j]]))
                    product_pairs[pair] = product_pairs.get(pair, 0) + 1
        
        self.recommendations = {str(k): v for k, v in sorted(product_pairs.items(), key=lambda x: x[1], reverse=True)}
        self.save_data(self.recommendations_file, self.recommendations)
        print("Product recommendations generated successfully!")

    def suggest_products(self, purchased_item):
        """Suggest related products based on previous purchases."""
        suggestions = []
        for pair, count in self.recommendations.items():
            pair_items = eval(pair)
            if purchased_item in pair_items:
                suggestions.append(pair_items[1] if pair_items[0] == purchased_item else pair_items[0])
        return suggestions[:3]

    def run(self):
        """Main function to handle product recommendations."""
        while True:
            action = input("Choose an action: generate, suggest, or quit: ")
            if action == "quit":
                break
            elif action == "generate":
                self.generate_recommendations()
            elif action == "suggest":
                item = input("Enter purchased product barcode: ")
                suggestions = self.suggest_products(item)
                if suggestions:
                    print("Recommended products:", suggestions)
                else:
                    print("No recommendations available.")
            else:
                print("Invalid action.")

if __name__ == "__main__":
    pre = ProductRecommendationEngine()
    pre.run()
