import tkinter as tk
from tkinter import messagebox
import threading
import time
from plyer import notification


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List with Reminders")
        self.root.geometry("400x400")

        self.task_input = tk.Entry(self.root, width=40)
        self.task_input.pack(pady=10)

        self.reminder_input = tk.Entry(self.root, width=20)
        self.reminder_input.insert(0, "Reminder in seconds")
        self.reminder_input.pack(pady=5)

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, height=10)
        self.task_listbox.pack(pady=20)

        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=5)

        self.tasks = []

    def add_task(self):
        task = self.task_input.get()
        reminder_time = self.reminder_input.get()

        if task == "":
            messagebox.showwarning("Warning", "You must enter a task.")
        else:
            self.tasks.append((task, reminder_time))
            self.task_listbox.insert(tk.END, task)
            self.task_input.delete(0, tk.END)
            self.reminder_input.delete(0, tk.END)

            try:
                reminder_time = int(reminder_time)
                threading.Thread(target=self.set_reminder, args=(task, reminder_time), daemon=True).start()
            except ValueError:
                messagebox.showwarning("Warning", "Reminder time must be an integer.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_listbox.delete(selected_task_index)
            del self.tasks[selected_task_index[0]]

    def set_reminder(self, task, reminder_time):
        time.sleep(reminder_time)
        notification.notify(
            title="Task Reminder",
            message=f"Reminder: {task}",
            timeout=5
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
