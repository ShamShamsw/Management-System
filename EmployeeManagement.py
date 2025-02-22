import json
from datetime import datetime

class EmployeeManagementSystem:
    def __init__(self, filename="employees.json"):
        self.filename = filename
        self.employees = self.load_data()

    def load_data(self):
        """Load employee data from a JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        """Save employee data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.employees, file, indent=4)

    def add_employee(self, emp_id, name, contact, role, hourly_wage):
        """Add a new employee profile."""
        if emp_id in self.employees:
            print("Employee already exists.")
            return
        self.employees[emp_id] = {
            "name": name,
            "contact": contact,
            "role": role,
            "hourly_wage": hourly_wage,
            "work_hours": 0,
            "clock_in_time": None,
            "leave_requests": []
        }
        self.save_data()
        print(f"Employee {name} added successfully.")

    def remove_employee(self, emp_id):
        """Remove an employee profile."""
        if emp_id in self.employees:
            del self.employees[emp_id]
            self.save_data()
            print("Employee removed successfully.")
        else:
            print("Error: Employee not found.")

    def clock_in(self, emp_id):
        """Clock in an employee."""
        if emp_id in self.employees:
            if self.employees[emp_id]['clock_in_time']:
                print("Error: Employee already clocked in.")
                return
            self.employees[emp_id]['clock_in_time'] = datetime.now().isoformat()
            self.save_data()
            print(f"{self.employees[emp_id]['name']} clocked in.")
        else:
            print("Error: Employee not found.")

    def clock_out(self, emp_id):
        """Clock out an employee and calculate work hours."""
        if emp_id in self.employees:
            if not self.employees[emp_id]['clock_in_time']:
                print("Error: Employee not clocked in.")
                return
            clock_in_time = datetime.fromisoformat(self.employees[emp_id]['clock_in_time'])
            work_hours = (datetime.now() - clock_in_time).seconds / 3600
            self.employees[emp_id]['work_hours'] += work_hours
            self.employees[emp_id]['clock_in_time'] = None
            self.save_data()
            print(f"{self.employees[emp_id]['name']} clocked out. Worked {work_hours:.2f} hours.")
        else:
            print("Error: Employee not found.")

    def calculate_payroll(self):
        """Generate payroll report."""
        print("\nPayroll Report:")
        for emp_id, data in self.employees.items():
            pay = data['work_hours'] * data['hourly_wage']
            print(f"{data['name']} - Hours: {data['work_hours']}, Pay: ${pay:.2f}")

    def request_leave(self, emp_id, reason):
        """Request leave for an employee."""
        if emp_id in self.employees:
            self.employees[emp_id]['leave_requests'].append({"reason": reason, "status": "Pending"})
            self.save_data()
            print("Leave request submitted.")
        else:
            print("Error: Employee not found.")

    def manage_leaves(self):
        """Approve or reject leave requests."""
        for emp_id, data in self.employees.items():
            for request in data['leave_requests']:
                if request['status'] == "Pending":
                    decision = input(f"Approve leave for {data['name']} (Reason: {request['reason']})? (y/n): ")
                    request['status'] = "Approved" if decision.lower() == 'y' else "Rejected"
        self.save_data()
        print("Leave requests processed.")


def main():
    system = EmployeeManagementSystem()
    
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Clock In")
        print("4. Clock Out")
        print("5. Generate Payroll Report")
        print("6. Request Leave")
        print("7. Manage Leaves")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            emp_id = input("Enter Employee ID: ")
            name = input("Enter Employee Name: ")
            contact = input("Enter Contact Info: ")
            role = input("Enter Role: ")
            try:
                hourly_wage = float(input("Enter Hourly Wage: "))
                system.add_employee(emp_id, name, contact, role, hourly_wage)
            except ValueError:
                print("Invalid wage input.")
        elif choice == '2':
            emp_id = input("Enter Employee ID to remove: ")
            system.remove_employee(emp_id)
        elif choice == '3':
            emp_id = input("Enter Employee ID to clock in: ")
            system.clock_in(emp_id)
        elif choice == '4':
            emp_id = input("Enter Employee ID to clock out: ")
            system.clock_out(emp_id)
        elif choice == '5':
            system.calculate_payroll()
        elif choice == '6':
            emp_id = input("Enter Employee ID: ")
            reason = input("Enter Leave Reason: ")
            system.request_leave(emp_id, reason)
        elif choice == '7':
            system.manage_leaves()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()