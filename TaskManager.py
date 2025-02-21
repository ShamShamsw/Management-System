import json

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, description):
        """Add a new task."""
        self.tasks.append({"title": title, "description": description, "completed": False})
        self.save_tasks()
        print(f"Task '{title}' added.")

    def remove_task(self, title):
        """Remove a task by title."""
        self.tasks = [task for task in self.tasks if task['title'] != title]
        self.save_tasks()
        print(f"Task '{title}' removed.")

    def display_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks available.")
        else:
            print("\nTask List:")
            for task in self.tasks:
                status = "Done" if task["completed"] else "Pending"
                print(f"{task['title']} - {task['description']} [{status}]")

    def mark_task_complete(self, title):
        """Mark a task as completed."""
        for task in self.tasks:
            if task['title'] == title:
                task['completed'] = True
                self.save_tasks()
                print(f"Task '{title}' marked as completed.")
                return
        print("Task not found.")


def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Display Tasks")
        print("4. Mark Task Complete")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            manager.add_task(title, description)
        elif choice == '2':
            title = input("Enter task title to remove: ")
            manager.remove_task(title)
        elif choice == '3':
            manager.display_tasks()
        elif choice == '4':
            title = input("Enter task title to mark complete: ")
            manager.mark_task_complete(title)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
