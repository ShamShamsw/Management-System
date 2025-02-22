import json
import datetime

class EmployeePerformanceSystem:
    def __init__(self, employees_file="employees.json", tasks_file="tasks.json", reviews_file="reviews.json"):
        self.employees_file = employees_file
        self.tasks_file = tasks_file
        self.reviews_file = reviews_file
        self.employees = self.load_data(self.employees_file)
        self.tasks = self.load_data(self.tasks_file)
        self.reviews = self.load_data(self.reviews_file)

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

    def add_employee(self, employee_id, name, role):
        """Add a new employee."""
        self.employees.append({"employee_id": employee_id, "name": name, "role": role, "tasks_completed": 0})
        self.save_data(self.employees_file, self.employees)
        print(f"Employee {name} added successfully!")

    def assign_task(self, employee_id, task_name, deadline):
        """Assign a task to an employee."""
        task = {"employee_id": employee_id, "task_name": task_name, "deadline": deadline, "completed": False}
        self.tasks.append(task)
        self.save_data(self.tasks_file, self.tasks)
        print(f"Task '{task_name}' assigned to employee {employee_id}.")

    def complete_task(self, employee_id, task_name):
        """Mark a task as completed and update productivity metrics."""
        for task in self.tasks:
            if task["employee_id"] == employee_id and task["task_name"] == task_name:
                task["completed"] = True
                for employee in self.employees:
                    if employee["employee_id"] == employee_id:
                        employee["tasks_completed"] += 1
                self.save_data(self.tasks_file, self.tasks)
                self.save_data(self.employees_file, self.employees)
                print(f"Task '{task_name}' marked as completed for employee {employee_id}.")
                return
        print("Task not found or already completed.")

    def conduct_review(self, employee_id, rating, feedback):
        """Conduct a performance review for an employee."""
        review = {"employee_id": employee_id, "rating": rating, "feedback": feedback, "date": str(datetime.datetime.now())}
        self.reviews.append(review)
        self.save_data(self.reviews_file, self.reviews)
        print(f"Performance review recorded for employee {employee_id}.")

    def run(self):
        """Main function to handle employee performance interactions."""
        while True:
            action = input("Choose an action: add_employee, assign_task, complete_task, conduct_review, or quit: ")
            if action == "quit":
                break
            elif action == "add_employee":
                employee_id = input("Enter employee ID: ")
                name = input("Enter employee name: ")
                role = input("Enter employee role: ")
                self.add_employee(employee_id, name, role)
            elif action == "assign_task":
                employee_id = input("Enter employee ID: ")
                task_name = input("Enter task name: ")
                deadline = input("Enter deadline (YYYY-MM-DD): ")
                self.assign_task(employee_id, task_name, deadline)
            elif action == "complete_task":
                employee_id = input("Enter employee ID: ")
                task_name = input("Enter task name: ")
                self.complete_task(employee_id, task_name)
            elif action == "conduct_review":
                employee_id = input("Enter employee ID: ")
                rating = int(input("Enter rating (1-5): "))
                feedback = input("Enter feedback: ")
                self.conduct_review(employee_id, rating, feedback)
            else:
                print("Invalid action.")

if __name__ == "__main__":
    eps = EmployeePerformanceSystem()
    eps.run()
