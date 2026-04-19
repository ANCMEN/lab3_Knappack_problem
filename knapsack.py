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
            return None, None, None, None
        
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
            

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()