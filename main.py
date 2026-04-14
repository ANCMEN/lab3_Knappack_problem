"""
Лабораторна робота №3.2
Тема: Моделювання задачі «Рюкзак» методом динамічного програмування
Методологія: Kanban
Реалізація: Python + tkinter
Виконав: Мусін Михайло Олександрович
"""

import tkinter as tk
from tkinter import ttk, messagebox

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задача «Рюкзак» - Динамічне програмування")
        self.root.geometry("1000x700")
        
        # Змінні для введення (K-01)
        self.n_var = tk.IntVar(value=4)
        self.W_var = tk.IntVar(value=10)
        self.weights_var = tk.StringVar(value="2,3,4,5")
        self.values_var = tk.StringVar(value="3,4,5,8")
        
        # Таблиця DP та результат
        self.dp = []
        self.selected_items = []
        
        # Словник тестових варіантів (K-07)
        self.test_variants = {
            "Варіант 1 (n=4,W=10)": {"n": 4, "W": 10, "w": "2,3,4,5", "v": "3,4,5,8"},
            "Варіант 2 (n=5,W=15)": {"n": 5, "W": 15, "w": "1,3,4,5,9", "v": "2,4,6,7,13"},
            "Варіант 5 (n=7,W=20)": {"n": 7, "W": 20, "w": "2,4,6,3,5,7,8", "v": "6,10,12,7,9,14,15"},
            "Варіант 10 (n=6,W=18)": {"n": 6, "W": 18, "w": "4,3,5,6,2,4", "v": "8,7,10,13,5,6"},
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Створення інтерфейсу (K-01)"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ліва панель — введення даних
        input_frame = ttk.LabelFrame(main_frame, text="Вхідні дані", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        row = 0
        
        # Кількість предметів
        ttk.Label(input_frame, text="Кількість предметів (n):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.n_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Місткість рюкзака
        ttk.Label(input_frame, text="Місткість рюкзака (W):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.W_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Ваги предметів
        ttk.Label(input_frame, text="Вага предметів (w[i]):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.weights_var, width=20).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Цінності предметів
        ttk.Label(input_frame, text="Цінність предметів (v[i]):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.values_var, width=20).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Вибір тестового варіанту (K-07)
        ttk.Label(input_frame, text="Тестовий варіант:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.variant_combo = ttk.Combobox(input_frame, values=list(self.test_variants.keys()), width=18)
        self.variant_combo.grid(row=row, column=1, padx=5, pady=5)
        self.variant_combo.bind("<<ComboboxSelected>>", self.load_test_variant)
        row += 1
        
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=15)
        row += 1
        
        # Кнопки (K-09)
        ttk.Button(input_frame, text="Розв'язати", command=self.solve_knapsack).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="Очистити таблицю", command=self.clear_table).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="За замовчуванням", command=self.reset_defaults).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="Вихід", command=self.root.quit).grid(row=row, column=0, columnspan=2, pady=20)
        
        # Права панель — результати
        result_frame = ttk.LabelFrame(main_frame, text="Результати", padding="5")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Рамка для таблиці DP (K-04)
        self.table_frame = ttk.Frame(result_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Рамка для результату (K-05)
        self.result_frame = ttk.LabelFrame(result_frame, text="Оптимальний набір", padding="5")
        self.result_frame.pack(fill=tk.X, pady=5)
        
        self.result_label = ttk.Label(self.result_frame, text="")
        self.result_label.pack()
        
        self.max_value_label = ttk.Label(self.result_frame, text="")
        self.max_value_label.pack()
    
    def load_test_variant(self, event=None):
        """Завантаження тестового варіанту (K-07)"""
        variant_name = self.variant_combo.get()
        if variant_name in self.test_variants:
            data = self.test_variants[variant_name]
            self.n_var.set(data["n"])
            self.W_var.set(data["W"])
            self.weights_var.set(data["w"])
            self.values_var.set(data["v"])
            self.clear_table()
    
    def parse_input(self):
        """Парсинг вхідних даних (K-02)"""
        try:
            n = self.n_var.get()
            W = self.W_var.get()
            weights = [int(x.strip()) for x in self.weights_var.get().split(',')]
            values = [int(x.strip()) for x in self.values_var.get().split(',')]
            
            if len(weights) != n or len(values) != n:
                raise ValueError(f"Кількість предметів має бути {n}")
            if W < 0:
                raise ValueError("Місткість рюкзака не може бути від'ємною")
            if any(w < 0 for w in weights):
                raise ValueError("Вага предметів не може бути від'ємною")
            if any(v < 0 for v in values):
                raise ValueError("Цінність предметів не може бути від'ємною")
            
            return n, W, weights, values
        except ValueError as e:
            messagebox.showerror("Помилка введення", str(e))  # K-08
            return None, None, None, None
    
    def solve_knapsack(self):
        """Розв'язання задачі рюкзак методом динамічного програмування (K-03)"""
        n, W, weights, values = self.parse_input()
        if n is None:
            return
        
        # Ініціалізація таблиці DP
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        
        # Заповнення таблиці
        for i in range(1, n + 1):
            for w in range(W + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], 
                                   dp[i-1][w - weights[i-1]] + values[i-1])
                else:
                    dp[i][w] = dp[i-1][w]
        
        self.dp = dp
        max_value = dp[n][W]
        
        # Відновлення оптимального набору (K-05)
        selected = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected.append(i-1)
                w -= weights[i-1]
        selected.reverse()
        self.selected_items = selected
        
        # Відображення результатів
        self.display_table(weights, values)
        self.display_result(selected, weights, values, max_value)
    
    def display_table(self, weights, values):
        """Відображення таблиці DP (K-04) з візуалізацією вибраних предметів (K-06)"""
        # Очищення попередньої таблиці
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        n = len(weights)
        W = len(self.dp[0]) - 1
        
        # Створення Treeview
        columns = ["i"] + [f"w={w}" for w in range(W + 1)]
        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=min(n+2, 20))
        
        # Заголовки
        tree.heading("i", text="i")
        for w in range(W + 1):
            tree.heading(f"w={w}", text=f"{w}")
            tree.column(f"w={w}", width=60, anchor="center")
        tree.column("i", width=40, anchor="center")
        
        # Додавання рядків з візуальним виділенням (K-06)
        for i in range(n + 1):
            row_values = [str(i)] + [str(self.dp[i][w]) for w in range(W + 1)]
            item = tree.insert("", "end", values=row_values)
            
            # Виділення кольором для обраних предметів
            if i > 0 and (i-1) in self.selected_items:
                tree.tag_configure(f"selected_{i}", background="#90EE90")
                tree.item(item, tags=(f"selected_{i}",))
        
        # Додавання скролбару
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def display_result(self, selected, weights, values, max_value):
        """Відображення оптимального набору предметів"""
        if not selected:
            self.result_label.config(text="Жоден предмет не вибрано")
            total_weight = 0
        else:
            items_text = []
            total_weight = 0
            for idx in selected:
                items_text.append(f"Предмет {idx+1} (вага={weights[idx]}, цінність={values[idx]})")
                total_weight += weights[idx]
            self.result_label.config(text="\n".join(items_text))
        
        self.max_value_label.config(text=f"Максимальна цінність: {max_value}\nЗагальна вага: {total_weight}")
    
    def clear_table(self):
        """Очищення таблиці та результатів (K-09)"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
        self.max_value_label.config(text="")
        self.dp = []
        self.selected_items = []
    
    def reset_defaults(self):
        """Скидання до значень за замовчуванням (K-09)"""
        self.n_var.set(4)
        self.W_var.set(10)
        self.weights_var.set("2,3,4,5")
        self.values_var.set("3,4,5,8")
        self.variant_combo.set("")
        self.clear_table()


def main():
    root = tk.Tk()
    app = KnapsackApp(root)
    
    # Центрування вікна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()