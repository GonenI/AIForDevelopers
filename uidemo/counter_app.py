import tkinter as tk
from tkinter import ttk

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Counter App")
        self.root.geometry("300x400")
        self.root.configure(bg='white')
        
        # Counter value
        self.counter = 3
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, bg='white', padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Counter display
        self.counter_label = tk.Label(
            self.main_frame, 
            text=str(self.counter),
            font=('Arial', 48, 'bold'),
            bg='white',
            fg='black'
        )
        self.counter_label.pack(pady=(20, 40))
        
        # Button frame
        self.button_frame = tk.Frame(self.main_frame, bg='white')
        self.button_frame.pack(pady=20)
        
        # Increment button (green with up arrow)
        self.inc_button = tk.Button(
            self.button_frame,
            text="▲",
            font=('Arial', 24, 'bold'),
            bg='lightgreen',
            fg='darkgreen',
            width=6,
            height=2,
            command=self.increment,
            relief='raised',
            bd=3
        )
        self.inc_button.pack(side='left', padx=10)
        
        # Decrement button (red with down arrow)
        self.dec_button = tk.Button(
            self.button_frame,
            text="▼",
            font=('Arial', 24, 'bold'),
            bg='lightcoral',
            fg='darkred',
            width=6,
            height=2,
            command=self.decrement,
            relief='raised',
            bd=3
        )
        self.dec_button.pack(side='left', padx=10)
        
        # Labels for buttons
        self.label_frame = tk.Frame(self.main_frame, bg='white')
        self.label_frame.pack(pady=10)
        
        self.inc_label = tk.Label(
            self.label_frame,
            text="inc",
            font=('Arial', 12),
            bg='white',
            fg='darkgreen'
        )
        self.inc_label.pack(side='left', padx=(25, 45))
        
        self.dec_label = tk.Label(
            self.label_frame,
            text="dec",
            font=('Arial', 12),
            bg='white',
            fg='darkred'
        )
        self.dec_label.pack(side='left', padx=(25, 45))
    
    def increment(self):
        """Increment the counter by 1"""
        self.counter += 1
        self.update_display()
    
    def decrement(self):
        """Decrement the counter by 1"""
        self.counter -= 1
        self.update_display()
    
    def update_display(self):
        """Update the counter display"""
        self.counter_label.config(text=str(self.counter))

def main():
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
