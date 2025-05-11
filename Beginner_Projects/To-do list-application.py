def add_task(tasks, task):
    tasks.append(task)
    print(f"\n ** Task '{task}' added successfully! **")

def remove_task(tasks, task):
    if task in tasks:
        tasks.remove(task)
        print(f"\n ** Task '{task}' removed successfully! **")
    else:
        print(f"\n ** Task '{task}' not found in the list. **")
        
def view_tasks(tasks):
    if not tasks:
        print("\n ** No tasks in the list. **")
    else:
        print("\n ** Tasks: **")
        for idx, task in enumerate(tasks, start=1):
            print(f"\n{idx}. {task}")

def main():
    tasks = []
    print("\nWelcome to the To-Do List Application!")

    while True:     
        print("\nSelect operation:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View Tasks")
        print("4. Exit")

        choice = input("Enter your choice: ")   
        
        if choice == '1':
            task = input("Enter the task to add: ")
            add_task(tasks, task)
        elif choice == '2':
            task = input("Enter the task to remove: ")
            remove_task(tasks, task)
        elif choice == '3':
            view_tasks(tasks)
        elif choice == '4':
            print("Exiting the application...")
            break    
        else:
            print("Invalid choice. Please enter a valid operation.")

if __name__ == "__main__":
    main()
