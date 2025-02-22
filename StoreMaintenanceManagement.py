import json
import datetime

class StoreMaintenanceSystem:
    def __init__(self, maintenance_file="maintenance.json", assets_file="assets.json", requests_file="requests.json"):
        self.maintenance_file = maintenance_file
        self.assets_file = assets_file
        self.requests_file = requests_file
        self.maintenance_schedule = self.load_data(self.maintenance_file)
        self.assets = self.load_data(self.assets_file)
        self.service_requests = self.load_data(self.requests_file)

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

    def schedule_maintenance(self, task, date, assigned_to):
        """Add a new maintenance task to the schedule."""
        task_entry = {
            "task": task,
            "date": date,
            "assigned_to": assigned_to,
            "status": "Scheduled"
        }
        self.maintenance_schedule.append(task_entry)
        self.save_data(self.maintenance_file, self.maintenance_schedule)
        print(f"Maintenance task '{task}' scheduled successfully!")

    def list_maintenance(self):
        """List all scheduled maintenance tasks."""
        print("Maintenance Schedule:")
        for task in self.maintenance_schedule:
            print(json.dumps(task, indent=4))

    def add_asset(self, name, quantity, condition):
        """Add a new store asset to inventory."""
        asset = {
            "name": name,
            "quantity": quantity,
            "condition": condition
        }
        self.assets.append(asset)
        self.save_data(self.assets_file, self.assets)
        print(f"Asset '{name}' added successfully!")

    def list_assets(self):
        """List all store assets."""
        print("Store Assets:")
        for asset in self.assets:
            print(json.dumps(asset, indent=4))

    def request_service(self, issue, reported_by, priority):
        """Submit a service request for store maintenance."""
        request = {
            "issue": issue,
            "reported_by": reported_by,
            "priority": priority,
            "status": "Pending"
        }
        self.service_requests.append(request)
        self.save_data(self.requests_file, self.service_requests)
        print(f"Service request for '{issue}' submitted successfully!")

    def list_requests(self):
        """List all service requests."""
        print("Service Requests:")
        for request in self.service_requests:
            print(json.dumps(request, indent=4))

    def run(self):
        """Main function to handle store maintenance and asset management interactions."""
        while True:
            action = input("Choose an action: schedule, list_maintenance, add_asset, list_assets, request_service, list_requests, or quit: ")
            if action == "quit":
                break
            elif action == "schedule":
                task = input("Enter maintenance task: ")
                date = input("Enter scheduled date (YYYY-MM-DD): ")
                assigned_to = input("Enter assigned person: ")
                self.schedule_maintenance(task, date, assigned_to)
            elif action == "list_maintenance":
                self.list_maintenance()
            elif action == "add_asset":
                name = input("Enter asset name: ")
                quantity = int(input("Enter quantity: "))
                condition = input("Enter condition: ")
                self.add_asset(name, quantity, condition)
            elif action == "list_assets":
                self.list_assets()
            elif action == "request_service":
                issue = input("Enter issue description: ")
                reported_by = input("Enter reporter name: ")
                priority = input("Enter priority (Low, Medium, High): ")
                self.request_service(issue, reported_by, priority)
            elif action == "list_requests":
                self.list_requests()
            else:
                print("Invalid action.")

if __name__ == "__main__":
    sms = StoreMaintenanceSystem()
    sms.run()