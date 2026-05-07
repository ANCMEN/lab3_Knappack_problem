import tkinter as tk
from tkinter import ttk, messagebox
"""Етап 1 (K-01): Базовий інтерфейс"""
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
        """K-07: Додавання тестового варіанту 14"""
        ttk.Label(input_frame, text="Тестовий варіант:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.variant_combo = ttk.Combobox(input_frame, values=["Варіант 14 (n=5, W=25)"], width=18)
        self.variant_combo.grid(row=row, column=1, padx=5, pady=5)
        self.variant_combo.set("Варіант 14 (n=5, W=25)")
        self.variant_combo.bind("<<ComboboxSelected>>", self.load_test_variant)
        row += 1

        """Етап 10 (K-10): Вибір методу та головний solve"""
        self.method_var = tk.StringVar(value="Dynamic Programming (DP)")
        ttk.Label(input_frame, text="Метод розв'язку:").grid(row=row, column=0, sticky=tk.W, pady=5)
        method_combo = ttk.Combobox(
            input_frame, 
            textvariable=self.method_var,
            values=[
                "Brute Force (перебір)",
                "Recursive (рекурсія)",
                "Dynamic Programming (DP)",
                "Greedy (жадібний)",
                "Branch and Bound (гілки та межі)"
            ],
            width=25
        )
        method_combo.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        """Етап 7 (K-09): Кнопки керування"""
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=15)
        row += 1
        
        ttk.Button(input_frame, text="Розв'язати", command=self.solve).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="Очистити таблицю", command=self.clear_table).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="За замовчуванням", command=self.reset_defaults).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(input_frame, text="Вихід", command=self.root.quit).grid(row=row, column=0, columnspan=2, pady=20)
        
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

    """Це методи для функціонування кнопок керування"""
    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
        self.max_value_label.config(text="")

    def reset_defaults(self):
        self.n_var.set(5)
        self.W_var.set(25)
        self.weights_var.set("8,1,4,7,8")
        self.values_var.set("9,9,15,9,11")
        self.clear_table()

    """метод для завантаження тестового варіанту"""
    def load_test_variant(self, event=None):
        self.n_var.set(5)
        self.W_var.set(25)
        self.weights_var.set("8,1,4,7,8")
        self.values_var.set("9,9,15,9,11")
        self.clear_table()

    """Етап 2 (K-02): Парсинг вхідних даних"""
    """Етап 4 (K-08): Обробка помилок (Було додано обробку негативних значень та помилок)"""
    def parse_input(self):
        try:
            n = self.n_var.get()
            W = self.W_var.get()
            weights = [int(x.strip()) for x in self.weights_var.get().split(',')]
            values = [int(x.strip()) for x in self.values_var.get().split(',')]
            
            if len(weights) != n or len(values) != n:
                raise ValueError(f"Кількість предметів має бути {n}")
            if W < 0 or any(w < 0 for w in weights) or any(v < 0 for v in values):
                raise ValueError("Негативні значення не дозволені")
            
            return n, W, weights, values
        except Exception as e:
            messagebox.showerror("Помилка введення", str(e))
            return None, None, None, None
        
    """Етап 3 (K-03): Всі 5 методів розв'язання"""        
    # ---------- 1. Brute Force ----------
    def solve_bruteforce(self, weights, values, n, W):
        best_value = 0
        best_combination = []
        for mask in range(1 << n):
            total_weight = 0
            total_value = 0
            current = []
            for i in range(n):
                if mask >> i & 1:
                    total_weight += weights[i]
                    total_value += values[i]
                    current.append(i)
            if total_weight <= W and total_value > best_value:
                best_value = total_value
                best_combination = current.copy()
        return None, best_value, best_combination

    # ---------- 2. Recursive ----------
    def solve_recursive(self, weights, values, n, W):
        def rec(i, remaining_w):
            if i == n or remaining_w <= 0:
                return 0, []
            val_no, items_no = rec(i+1, remaining_w)
            if weights[i] <= remaining_w:
                val_yes, items_yes = rec(i+1, remaining_w - weights[i])
                val_yes += values[i]
                if val_yes > val_no:
                    return val_yes, items_yes + [i]
            return val_no, items_no
        max_value, selected = rec(0, W)
        selected.sort()
        return None, max_value, selected

    # ---------- 3. Dynamic Programming ----------
    def solve_DP(self, weights, values, n, W):
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for w in range(W + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
                else:
                    dp[i][w] = dp[i-1][w]
        max_value = dp[n][W]
        selected = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected.append(i-1)
                w -= weights[i-1]
        selected.reverse()
        return dp, max_value, selected

    # ---------- 4. Greedy ----------
    def solve_greedy(self, weights, values, n, W):
        items = [(values[i], weights[i], i) for i in range(n)]
        items.sort(key=lambda x: x[0]/x[1] if x[1]!=0 else 0, reverse=True)
        selected = []
        total_weight = 0
        total_value = 0
        for v, w, idx in items:
            if total_weight + w <= W:
                selected.append(idx)
                total_weight += w
                total_value += v
        selected.sort()
        return None, total_value, selected

    # ---------- 5. Branch and Bound ----------
    def solve_branch_bound(self, weights, values, n, W):
        items = sorted([(values[i], weights[i], i) for i in range(n)],
                    key=lambda x: x[0]/x[1] if x[1]!=0 else 0, reverse=True)
        sorted_vals = [v for v, w, i in items]
        sorted_weights = [w for v, w, i in items]
        original_indices = [i for v, w, i in items]
        
        best_value = 0
        best_combination = []
        
        def bound(i, current_w, current_v):
            if current_w > W:
                return 0
            remaining_w = W - current_w
            bound_val = current_v
            j = i
            while j < n and sorted_weights[j] <= remaining_w:
                bound_val += sorted_vals[j]
                remaining_w -= sorted_weights[j]
                j += 1
            if j < n:
                bound_val += (remaining_w / sorted_weights[j]) * sorted_vals[j]
            return bound_val
        
        def backtrack(i, current_w, current_v, taken):
            nonlocal best_value, best_combination
            if i == n:
                if current_v > best_value:
                    best_value = current_v
                    best_combination = taken.copy()
                return
            if bound(i, current_w, current_v) <= best_value:
                return
            if current_w + sorted_weights[i] <= W:
                taken.append(original_indices[i])
                backtrack(i+1, current_w + sorted_weights[i], current_v + sorted_vals[i], taken)
                taken.pop()
            backtrack(i+1, current_w, current_v, taken)
        
        backtrack(0, 0, 0, [])
        best_combination.sort()
        return None, best_value, best_combination
    
""""K-11: Базовий клас анімації AnimationController"""    
class AnimationController:
    """Контролер анімації для всіх алгоритмів"""
    
    def __init__(self, app):
        self.app = app
        self.is_running = False
        self.is_paused = False
        self.speed = 500  # мс між кроками
        self.current_step = 0
        self.total_steps = 0
        self.after_id = None
        
    def start(self):
        """Запуск анімації"""
        if self.is_paused:
            self.is_paused = False
            self.resume()
        elif not self.is_running:
            self.is_running = True
            self.current_step = 0
            self.next_step()
    
    def pause(self):
        """Пауза"""
        self.is_paused = True
        if self.after_id:
            self.app.root.after_cancel(self.after_id)
    
    def resume(self):
        """Продовження"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.next_step()
    
    def stop(self):
        """Зупинка"""
        self.is_running = False
        self.is_paused = False
        if self.after_id:
            self.app.root.after_cancel(self.after_id)
    
    def next_step(self):
        """Виконання одного кроку"""
        if not self.is_running or self.is_paused:
            return
        if self.current_step >= self.total_steps:
            self.stop()
            self.app.update_animation_status("Анімація завершена!")
            return
        
        # Викликаємо метод анімації поточного алгоритму
        if hasattr(self.app, f"animate_step_{self.current_step}"):
            getattr(self.app, f"animate_step_{self.current_step}")()
        
        self.current_step += 1
        self.app.update_progress(self.current_step, self.total_steps)
        
        # Плануємо наступний крок
        self.after_id = self.app.root.after(self.speed, self.next_step)
    
    def set_speed(self, speed):
        """Зміна швидкості"""
        speed_map = {"Повільна": 800, "Нормальна": 400, "Швидка": 150, "Дуже швидка": 50}
        self.speed = speed_map.get(speed, 400) 
          
    """K-12: Анімація Brute Force"""
        
    def animate_bruteforce(self):
        """Підготовка анімації для Brute Force"""
        n = self.n_var.get()
        self.animation_controller.total_steps = (1 << n)  # 2^n кроків
        self.animation_controller.current_step = 0
        self.animation_controller.is_running = True
        
        # Зберігаємо дані для анімації
        self.bf_best_value = 0
        self.bf_best_combination = []
        self.bf_weights = None
        self.bf_values = None
        self.bf_n = n
        self.bf_W = self.W_var.get()
        
        # Очищуємо Canvas
        self.clear_animation_canvas()
        
        # Запускаємо анімацію
        self.animation_controller.next_step()

    def animate_step_bruteforce(self, mask):
        """Один крок анімації Brute Force"""
        n, W = self.bf_n, self.bf_W
        weights, values = self.bf_weights, self.bf_values
        
        total_weight = 0
        total_value = 0
        current_items = []
        
        for i in range(n):
            if mask >> i & 1:
                total_weight += weights[i]
                total_value += values[i]
                current_items.append(i+1)
        
        # Оновлюємо Canvas
        self.update_animation_canvas({
            "mask": bin(mask),
            "mask_dec": mask,
            "items": current_items,
            "weight": total_weight,
            "value": total_value,
            "best_value": self.bf_best_value,
            "best_items": [i+1 for i in self.bf_best_combination]
        })
        
        # Оновлюємо прогрес
        self.update_progress(mask + 1, self.animation_controller.total_steps)
        
        # Оновлюємо найкращий результат
        if total_weight <= W and total_value > self.bf_best_value:
            self.bf_best_value = total_value
            self.bf_best_combination = [i for i in range(n) if (mask >> i) & 1]
            # Візуально виділити новий найкращий набір
            self.highlight_best_set()

    def render_bruteforce_frame(self, data):
        """Відображення одного кадру Brute Force"""
        canvas = self.animation_canvas
        canvas.delete("all")
        
        width, height = 600, 150
        canvas.config(width=width, height=height)
        
        # Заголовок
        canvas.create_text(10, 15, anchor="nw", text=f"Маска: {data['mask']} ({data['mask_dec']})", font=("Arial", 12, "bold"))
        canvas.create_text(10, 40, anchor="nw", text=f"Поточні предмети: {data['items']}")
        canvas.create_text(10, 65, anchor="nw", text=f"Вага: {data['weight']} / {self.bf_W}")
        canvas.create_text(10, 90, anchor="nw", text=f"Цінність: {data['value']}")
        
        # Найкращий результат
        canvas.create_text(300, 40, anchor="nw", text=f"Найкраща цінність: {data['best_value']}", fill="green")
        canvas.create_text(300, 65, anchor="nw", text=f"Найкращий набір: {data['best_items']}", fill="green")
        
        # Прогрес-бар
        progress = data['mask_dec'] / self.animation_controller.total_steps
        canvas.create_rectangle(10, 120, 10 + 580 * progress, 140, fill="blue", outline="")
        canvas.create_text(300, 130, text=f"{int(progress*100)}%", font=("Arial", 10)) 
    """K-13: Анімація DP з покроковим заповненням таблиці"""
    def animate_DP(self):
        """Підготовка анімації для DP"""
        n, W, weights, values = self.parse_input()
        if n is None:
            return
        
        self.dp_weights = weights
        self.dp_values = values
        self.dp_n = n
        self.dp_W = W
        
        # Ініціалізуємо таблицю DP
        self.dp_table = [[0] * (W + 1) for _ in range(n + 1)]
        
        # Кроки: для кожної клітинки (i, w)
        self.animation_controller.total_steps = (n + 1) * (W + 1)
        self.animation_controller.current_step = 0
        
        self.dp_i = 1
        self.dp_w = 0
        
        self.clear_animation_canvas()
        self.display_table(self.dp_weights, self.dp_values, self.dp_table, [])
        
        self.animation_controller.start()

def animate_step_DP(self):
    """Один крок анімації DP (заповнення однієї клітинки)"""
    i, w = self.dp_i, self.dp_w
    weights, values = self.dp_weights, self.dp_values
    W = self.dp_W
    
    if i > self.dp_n:
        # Анімація завершена — показуємо результат
        self.finish_DP_animation()
        return
    
    # Обчислюємо значення для dp[i][w]
    if weights[i-1] <= w:
        self.dp_table[i][w] = max(self.dp_table[i-1][w], 
                                   self.dp_table[i-1][w - weights[i-1]] + values[i-1])
    else:
        self.dp_table[i][w] = self.dp_table[i-1][w]
    
    # Оновлюємо відображення таблиці з підсвіткою активної клітинки
    self.update_table_with_highlight(i, w)
    
    self.update_progress(self.animation_controller.current_step, self.animation_controller.total_steps)
    
    # Переходимо до наступної клітинки
    if w < W:
        self.dp_w += 1
    else:
        self.dp_i += 1
        self.dp_w = 0

def update_table_with_highlight(self, active_i, active_w):
    """Відображення таблиці з виділенням активної клітинки"""
    for widget in self.table_frame.winfo_children():
        widget.destroy()
    
    n, W = self.dp_n, self.dp_W
    columns = ["i"] + [f"w={w}" for w in range(W + 1)]
    tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=min(n+2, 20))
    
    tree.heading("i", text="i")
    for w in range(W + 1):
        tree.heading(f"w={w}", text=f"{w}")
        tree.column(f"w={w}", width=50, anchor="center")
    tree.column("i", width=40, anchor="center")
    
    for i in range(n + 1):
        row_values = [str(i)] + [str(self.dp_table[i][w]) for w in range(W + 1)]
        item = tree.insert("", "end", values=row_values)
        
        # Виділяємо активну клітинку червоним
        if i == active_i:
            tree.tag_configure("active_cell", background="#ffcccc")
            tree.item(item, tags=("active_cell",))
        # Виділяємо вибрані предмети зеленим (після завершення)
        elif active_i == -1 and i > 0 and (i-1) in self.selected_items:
            tree.tag_configure(f"selected_{i}", background="#90EE90")
            tree.item(item, tags=(f"selected_{i}",))
    
    scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Для підсвітки конкретної комірки додаємо додатковий рядок
    if active_i >= 0:
        self.highlight_cell(tree, active_i, active_w)

def highlight_cell(self, tree, i, w):
    """Підсвітка конкретної комірки в Treeview (складно через обмеження Treeview)"""
    # Альтернатива: показувати активну комірку в окремому Canvas
    self.show_active_cell_in_canvas(i, w)

    """K-14: Панель керування анімацією (Play/Pause/Step/Speed)"""
def setup_animation_panel(self, parent):
    """Створення панелі керування анімацією"""
    panel = ttk.LabelFrame(parent, text="Керування анімацією", padding="5")
    panel.pack(fill=tk.X, pady=5)
    
    # Canvas для візуалізації
    self.animation_canvas = tk.Canvas(panel, height=150, bg="white", relief=tk.SUNKEN, bd=1)
    self.animation_canvas.pack(fill=tk.X, pady=5, padx=5)
    
    # Кнопки керування
    btn_frame = ttk.Frame(panel)
    btn_frame.pack()
    
    ttk.Button(btn_frame, text="⏸ Пауза", command=self.animation_controller.pause).pack(side=tk.LEFT, padx=2)
    ttk.Button(btn_frame, text="▶ Старт", command=self.animation_controller.start).pack(side=tk.LEFT, padx=2)
    ttk.Button(btn_frame, text="⏩ Крок", command=self.animation_controller.next_step).pack(side=tk.LEFT, padx=2)
    ttk.Button(btn_frame, text="🔄 Скинути", command=self.reset_animation).pack(side=tk.LEFT, padx=2)
    
    # Вибір швидкості
    ttk.Label(btn_frame, text="Швидкість:").pack(side=tk.LEFT, padx=(10, 2))
    self.speed_var = tk.StringVar(value="Нормальна")
    speed_combo = ttk.Combobox(btn_frame, textvariable=self.speed_var, 
                                values=["Повільна", "Нормальна", "Швидка", "Дуже швидка"], 
                                width=12, state="readonly")
    speed_combo.pack(side=tk.LEFT, padx=2)
    speed_combo.bind("<<ComboboxSelected>>", self.change_animation_speed)
    
    # Прогрес-бар
    self.progress_var = tk.IntVar(value=0)
    self.progress_bar = ttk.Progressbar(panel, variable=self.progress_var, maximum=100, length=400)
    self.progress_bar.pack(pady=5)
    
    self.status_label = ttk.Label(panel, text="Готовий до анімації")
    self.status_label.pack()

def change_animation_speed(self, event=None):
    """Зміна швидкості анімації"""
    self.animation_controller.set_speed(self.speed_var.get())

def update_progress(self, current, total):
    """Оновлення прогрес-бару"""
    percent = int(current / total * 100) if total > 0 else 0
    self.progress_var.set(percent)
    self.status_label.config(text=f"Крок {current} з {total} ({percent}%)")

    
    """Етап 5 (K-04): Відображення таблиці DP"""    

    def display_table(self, weights, values, dp, selected):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        n = len(weights)
        W = len(dp[0]) - 1
        columns = ["i"] + [f"w={w}" for w in range(W + 1)]
        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=min(n+2, 20))
        
        tree.heading("i", text="i")
        for w in range(W + 1):
            tree.heading(f"w={w}", text=f"{w}")
            tree.column(f"w={w}", width=60, anchor="center")
        tree.column("i", width=40, anchor="center")
        
        """Етап 8 (K-06): Візуалізація вибраних предметів"""
        for i in range(n + 1):
            row_values = [str(i)] + [str(dp[i][w]) for w in range(W + 1)]
            item = tree.insert("", "end", values=row_values)
            if i > 0 and (i-1) in selected:
                tree.tag_configure(f"selected_{i}", background="#90EE90")
                tree.item(item, tags=(f"selected_{i}",))

        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    """Етап 6 (K-05): Відновлення набору та виведення результату""" 
    def display_result(self, selected, weights, values, max_value):
        current_text = self.result_label.cget("text")
        
        if not selected:
            items_text = "Жоден предмет не вибрано"
            total_weight = 0
        else:
            items_lines = []
            total_weight = 0
            for idx in selected:
                items_lines.append(f"Предмет {idx+1} (вага={weights[idx]}, цінність={values[idx]})")
                total_weight += weights[idx]
            items_text = "\n".join(items_lines)
        
        if current_text and "[WARNING]" in current_text:
            full_text = current_text + "\n\n" + items_text
        else:
            full_text = items_text
        
        self.result_label.config(text=full_text)
        self.max_value_label.config(text=f"Максимальна цінність: {max_value}\nЗагальна вага: {total_weight}")
   
    """ Повністю функціональний метод solve """
    def solve(self):
        n, W, weights, values = self.parse_input()
        if n is None:
            return
        
        method = self.method_var.get()
        self.clear_table()
        
        self.result_label.config(text="")
        self.max_value_label.config(text="")
        
        if method == "Brute Force (перебір)":
            dp, max_value, selected = self.solve_bruteforce(weights, values, n, W)
            self.result_label.config(text="[WARNING] Метод перебору не будує таблицю DP", foreground="orange")
        elif method == "Recursive (рекурсія)":
            dp, max_value, selected = self.solve_recursive(weights, values, n, W)
            self.result_label.config(text="[WARNING] Рекурсивний метод не будує таблицю DP", foreground="orange")
        elif method == "Dynamic Programming (DP)":
            dp, max_value, selected = self.solve_DP(weights, values, n, W)
            self.display_table(weights, values, dp, selected)
            self.result_label.config(text=" Таблиця DP побудована", foreground="green")
        elif method == "Greedy (жадібний)":
            dp, max_value, selected = self.solve_greedy(weights, values, n, W)
            self.result_label.config(text="[WARNING] Жадібний алгоритм не будує таблицю DP", foreground="orange")
        elif method == "Branch and Bound (гілки та межі)":
            dp, max_value, selected = self.solve_branch_bound(weights, values, n, W)
            self.result_label.config(text="[WARNING] Метод гілок та меж не будує таблицю DP", foreground="orange")
        else:
            return
        
        self.display_result(selected, weights, values, max_value)       

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()