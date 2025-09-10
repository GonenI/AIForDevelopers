import tkinter as tk

class CounterApp:
    def __init__(self, root):
        self.count = 0

        # Create a label to display the count
        self.label = tk.Label(root, text=f"Green Count: {self.count}", font=("Arial", 16), fg="green")
        self.label.pack(pady=10)

        # Create an increment button
        self.increment_button = tk.Button(
            root, text="INC", font=("Arial", 16), bg="red", fg="white", command=self.increment_count
        )
        self.increment_button.pack(pady=10)

    def increment_count(self):
        self.count += 1
        self.label.config(text=f"Green Count: {self.count}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Counter UI")
    app = CounterApp(root)
    root.mainloop()
