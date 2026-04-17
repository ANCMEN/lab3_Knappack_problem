import tkinter as tk
from tkinter import ttk

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задача «Рюкзак» — 5 методів")
        self.root.geometry("1050x750")
        
        self.n_var = tk.IntVar(value=5)
        self.W_var = tk.IntVar(value=25)
        self.weights_var = tk.StringVar(value="8,1,4,7,8")
        self.values_var = tk.StringVar(value="9,9,15,9,11")
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text="Вхідні дані", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        row = 0
        ttk.Label(input_frame, text="Кількість предметів (n):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.n_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Місткість рюкзака (W):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.W_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Вага предметів (w[i]):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.weights_var, width=20).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Цінність предметів (v[i]):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.values_var, width=20).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        result_frame = ttk.LabelFrame(main_frame, text="Результати", padding="5")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.table_frame = ttk.Frame(result_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_frame = ttk.LabelFrame(result_frame, text="Оптимальний набір", padding="5")
        self.result_frame.pack(fill=tk.X, pady=5)
        
        self.result_label = ttk.Label(self.result_frame, text="")
        self.result_label.pack()
        
        self.max_value_label = ttk.Label(self.result_frame, text="")
        self.max_value_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()