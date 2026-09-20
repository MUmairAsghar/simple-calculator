import ast
import math
import operator
import tkinter as tk


class SafeEvaluator:
	

	def __init__(self, angle_mode="DEG"):
		self.angle_mode = angle_mode

	def _angle(self, value):
		return math.radians(value) if self.angle_mode == "DEG" else value

	def _from_angle(self, value):
		result = math.degrees(value) if self.angle_mode == "DEG" else value
		return result

	def evaluate(self, expression, answer=0.0):
		expression = expression.replace("^", "**").replace("pi", "PI")
		tree = ast.parse(expression, mode="eval")
		return self._visit(tree.body, answer)

	def _visit(self, node, answer):
		if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
			return node.value
		if isinstance(node, ast.Name):
			constants = {"PI": math.pi, "E": math.e, "e": math.e, "Ans": answer}
			if node.id in constants:
				return constants[node.id]
			raise ValueError("Unknown symbol")
		if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.USub, ast.UAdd):
			value = self._visit(node.operand, answer)
			return -value if isinstance(node.op, ast.USub) else value
		if isinstance(node, ast.BinOp) and type(node.op) in OPERATOR_MAP:
			left = self._visit(node.left, answer)
			right = self._visit(node.right, answer)
			return OPERATOR_MAP[type(node.op)](left, right)
		if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
			name = node.func.id
			if name not in self._functions():
				raise ValueError("Unknown function")
			args = [self._visit(arg, answer) for arg in node.args]
			return self._functions()[name](*args)
		raise ValueError("Invalid expression")

	def _functions(self):
		return {
			"sin": lambda x: math.sin(self._angle(x)),
			"cos": lambda x: math.cos(self._angle(x)),
			"tan": lambda x: math.tan(self._angle(x)),
			"asin": lambda x: self._from_angle(math.asin(x)),
			"acos": lambda x: self._from_angle(math.acos(x)),
			"atan": lambda x: self._from_angle(math.atan(x)),
			"sqrt": math.sqrt,
			"cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
			"log": math.log10,
			"ln": math.log,
			"abs": abs,
			"exp": math.exp,
			"floor": math.floor,
			"ceil": math.ceil,
			"fact": math.factorial,
		}


OPERATOR_MAP = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
	ast.Pow: operator.pow,
	ast.Mod: operator.mod,
}


class CalculatorApp:
	COLORS = {
		"bg": "#11151c",
		"panel": "#191f29",
		"display": "#0b0e13",
		"text": "#f4f7fb",
		"muted": "#8f9bad",
		"key": "#242c38",
		"key_hover": "#303b4b",
		"operator": "#294961",
		"accent": "#54d6b1",
		"danger": "#ff7d87",
		"border": "#303948",
	}

	def __init__(self, root):
		self.root = root
		self.root.title("Axiom | Scientific Calculator")
		self.root.geometry("920x640")
		self.root.minsize(760, 560)
		self.root.configure(bg=self.COLORS["bg"])
		self.expression = tk.StringVar()
		self.result = tk.StringVar(value="0")
		self.status = tk.StringVar(value="Ready")
		self.angle_mode = tk.StringVar(value="DEG")
		self.memory = 0.0
		self.answer = 0.0
		self.evaluator = SafeEvaluator()
		self.history = []
		self._build_ui()
		self._bind_keys()

	def _build_ui(self):
		header = tk.Frame(self.root, bg=self.COLORS["bg"])
		header.pack(fill="x", padx=28, pady=(24, 12))
		tk.Label(header, text="AXIOM", font=("Segoe UI", 18, "bold"), fg=self.COLORS["accent"], bg=self.COLORS["bg"]).pack(side="left")
		tk.Label(header, text="SCIENTIFIC CALCULATOR", font=("Segoe UI", 10, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["bg"]).pack(side="left", padx=12, pady=(5, 0))
		mode = tk.Frame(header, bg=self.COLORS["bg"])
		mode.pack(side="right")
		tk.Label(mode, text="ANGLE", font=("Segoe UI", 9, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["bg"]).pack(side="left", padx=8)
		for value in ("DEG", "RAD"):
			tk.Radiobutton(mode, text=value, variable=self.angle_mode, value=value, command=self._angle_changed, indicatoron=False, width=5, font=("Segoe UI", 9, "bold"), fg=self.COLORS["text"], bg=self.COLORS["key"], selectcolor=self.COLORS["operator"], activebackground=self.COLORS["key_hover"], activeforeground=self.COLORS["text"], relief="flat", bd=0, pady=5).pack(side="left", padx=2)

		display = tk.Frame(self.root, bg=self.COLORS["display"], highlightbackground=self.COLORS["border"], highlightthickness=1)
		display.pack(fill="x", padx=28, pady=(0, 20))
		tk.Label(display, textvariable=self.status, font=("Segoe UI", 9), fg=self.COLORS["muted"], bg=self.COLORS["display"], anchor="e").pack(fill="x", padx=20, pady=(14, 0))
		tk.Entry(display, textvariable=self.expression, font=("Consolas", 23), justify="right", relief="flat", bd=0, fg=self.COLORS["text"], insertbackground=self.COLORS["accent"], bg=self.COLORS["display"]).pack(fill="x", padx=18, pady=(8, 2), ipady=8)
		tk.Label(display, textvariable=self.result, font=("Consolas", 31, "bold"), fg=self.COLORS["accent"], bg=self.COLORS["display"], anchor="e").pack(fill="x", padx=20, pady=(0, 16))

		body = tk.Frame(self.root, bg=self.COLORS["bg"])
		body.pack(fill="both", expand=True, padx=28)
		keys = tk.Frame(body, bg=self.COLORS["bg"])
		keys.pack(side="left", fill="both", expand=True)
		history_panel = tk.Frame(body, bg=self.COLORS["panel"], width=235, highlightbackground=self.COLORS["border"], highlightthickness=1)
		history_panel.pack(side="right", fill="y", padx=(18, 0))
		history_panel.pack_propagate(False)
		tk.Label(history_panel, text="HISTORY", font=("Segoe UI", 10, "bold"), fg=self.COLORS["text"], bg=self.COLORS["panel"], anchor="w").pack(fill="x", padx=14, pady=(14, 8))
		self.history_list = tk.Listbox(history_panel, bg=self.COLORS["panel"], fg=self.COLORS["muted"], selectbackground=self.COLORS["operator"], selectforeground=self.COLORS["text"], relief="flat", bd=0, highlightthickness=0, font=("Consolas", 10), activestyle="none")
		self.history_list.pack(fill="both", expand=True, padx=8)
		tk.Button(history_panel, text="CLEAR HISTORY", command=self._clear_history, font=("Segoe UI", 9, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["key"], activebackground=self.COLORS["key_hover"], activeforeground=self.COLORS["text"], relief="flat", bd=0, pady=8).pack(fill="x", padx=10, pady=10)

		layout = [
			[("MC", "memory_clear", "muted"), ("MR", "memory_recall", "muted"), ("M+", "memory_add", "muted"), ("M-", "memory_subtract", "muted"), ("AC", "clear", "danger"), ("DEL", "delete", "danger")],
			[("sin", "sin(", "function"), ("cos", "cos(", "function"), ("tan", "tan(", "function"), ("ln", "ln(", "function"), ("log", "log(", "function"), ("sqrt", "sqrt(", "function")],
			[("7", "7", "number"), ("8", "8", "number"), ("9", "9", "number"), ("(", "(", "number"), (")", ")", "number"), ("/", "/", "operator")],
			[("4", "4", "number"), ("5", "5", "number"), ("6", "6", "number"), ("^", "^", "operator"), ("%", "%", "operator"), ("*", "*", "operator")],
			[("1", "1", "number"), ("2", "2", "number"), ("3", "3", "number"), ("pi", "pi", "function"), ("e", "e", "function"), ("-", "-", "operator")],
			[("0", "0", "number"), (".", ".", "number"), ("Ans", "Ans", "function"), ("+", "+", "operator"), ("=", "equals", "equals")],
		]
		for row_index, row in enumerate(layout):
			keys.grid_rowconfigure(row_index, weight=1)
			for column_index, (label, value, kind) in enumerate(row):
				keys.grid_columnconfigure(column_index, weight=1)
				if value in ("memory_clear", "memory_recall", "memory_add", "memory_subtract", "clear", "delete", "equals"):
					command = getattr(self, f"_{value}")
				else:
					command = lambda item=value: self._insert(item)
				bg = self.COLORS["operator"] if kind == "operator" else self.COLORS["key"]
				fg = self.COLORS["accent"] if kind in ("function", "equals") else self.COLORS["danger"] if kind == "danger" else self.COLORS["muted"] if kind == "muted" else self.COLORS["text"]
				button = tk.Button(keys, text=label, command=command, font=("Segoe UI", 11, "bold"), fg=fg, bg=bg, activeforeground=self.COLORS["text"], activebackground=self.COLORS["key_hover"], relief="flat", bd=0, highlightthickness=0)
				button.grid(row=row_index, column=column_index, sticky="nsew", padx=4, pady=4, ipadx=3, ipady=9)

			self.status.set(f"{self.angle_mode.get()}  |  Calculated")
			self.history.insert(0, (expression, formatted))
			self.history_list.insert(0, f"{expression} = {formatted}")
			self.expression.set("")
		except (ValueError, SyntaxError, TypeError, ZeroDivisionError, OverflowError):
			self.result.set("Error")
			self.status.set("Check expression")

	@staticmethod
	def _format(value):
		if value == int(value):
			return f"{int(value):,}"
		return f"{value:,.12g}"

	def _angle_changed(self):
		self.status.set(f"Angle mode: {self.angle_mode.get()}")

	def _clear_history(self):
		self.history.clear()
		self.history_list.delete(0, tk.END)

	def _memory_clear(self):
		self.memory = 0.0
		self.status.set("Memory cleared")

	def _memory_recall(self):
		self._insert(self._format(self.memory).replace(",", ""))

	def _memory_add(self):
		self.memory += self.answer
		self.status.set("Added answer to memory")

	def _memory_subtract(self):
		self.memory -= self.answer
		self.status.set("Subtracted answer from memory")


def main():
	root = tk.Tk()
	CalculatorApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
