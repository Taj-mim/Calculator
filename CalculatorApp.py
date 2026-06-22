from ast import expr
from pydoc import text
import tkinter as tk
import math
from unicodedata import name

BG = "#f5f5f5"          
BTN = "#ffffff"         
BTN_HOVER = "#e8e8e8"   
TEXT = "#000000"        
ACCENT = "#4f7cff"
OP = "#ff9500"

class Calculator:
    
 
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG)
        self.functions = {
            "sin": "math.sin",
            "cos": "math.cos",
            "tan": "math.tan"
            }
        self.ans = 0
        self.reset_next = False
        self.display = tk.Entry(
            root,
            font=("Arial", 24),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            bd=0,
            justify="right"
        )
        self.display.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="nsew",
            ipadx=10,
            ipady=25,
            padx=10,
            pady=10
        )
    def format_expression(self, expr):
            import re

            # add math prefix
            expr = expr.replace("sin", "math.sin")
            expr = expr.replace("cos", "math.cos")
            expr = expr.replace("tan", "math.tan")

            # auto add brackets: math.cos 30 → math.cos(30)
            expr = re.sub(r"(math\.(sin|cos|tan))\s+([0-9\.]+)", r"\1(\3)", expr)

            return expr

    def click(self, value):
        if self.reset_next:
            self.display.delete(0, tk.END)
            self.reset_next = False
        self.display.insert(tk.END, value)

    def clear(self):
        self.display.delete(0, tk.END)

    def delete_one(self):
        text = self.display.get()
        if text:   
         self.display.delete(len(text)-1, tk.END)
    def use_ans(self):
        if self.reset_next:
            self.display.delete(0, tk.END)
            self.reset_next = False
        self.display.insert(tk.END, str(self.ans))
    def func_click(self, name):
         if self.reset_next:
            self.display.delete(0, tk.END)
            self.reset_next = False

         self.display.insert(tk.END, name + "(")
    def equal(self):
         try:
            expr = self.display.get()

        # Convert trig functions to degree mode
            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")

                # Auto-close missing brackets
            open_brackets = expr.count("(")
            close_brackets = expr.count(")")
            expr += ")" * (open_brackets - close_brackets)

            result = eval(expr, {"__builtins__": {}, "math": math})

                # Remove tiny floating-point errors
            if abs(result) < 1e-10:
                    result = 0
            result = round(result, 10)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            self.ans = result
            self.reset_next = True

         except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "error")
            self.reset_next = True
# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("360x600")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

calc = Calculator(root)

# 🔥 FIX GRID SCALING (IMPORTANT)
for i in range(4):
    root.columnconfigure(i, weight=1)
for i in range(9):
    root.rowconfigure(i, weight=1)


# ---------------- BUTTON STYLE ----------------
def btn(text, cmd, r, c, color):
    tk.Button(
        root,
        text=text,
        command=cmd,
        bg=color,
        fg="#000000" if color != OP else "white",
        activebackground=BTN_HOVER,
        activeforeground="#000000" if color != OP else "white",
        bd=0,
        relief="flat",
        font=("Arial", 14, "bold"),
        cursor="hand2"
    ).grid(
        row=r,
        column=c,
        sticky="nsew",
        padx=4,
        pady=4
    )
# ---------------- LAYOUT (REAL CALCULATOR STYLE) ----------------

# Row 1
btn("C", calc.clear, 1, 0, BTN)
btn("⌫", calc.delete_one, 1, 1, BTN)
btn("(", lambda: calc.click("("), 1, 2, BTN)
btn(")", lambda: calc.click(")"), 1, 3, BTN)

# Row 2
btn("7", lambda: calc.click("7"), 2, 0, BTN)
btn("8", lambda: calc.click("8"), 2, 1, BTN)
btn("9", lambda: calc.click("9"), 2, 2, BTN)
btn("/", lambda: calc.click("/"), 2, 3, OP)

# Row 3
btn("4", lambda: calc.click("4"), 3, 0, BTN)
btn("5", lambda: calc.click("5"), 3, 1, BTN)
btn("6", lambda: calc.click("6"), 3, 2, BTN)
btn("*", lambda: calc.click("*"), 3, 3, OP)

# Row 4
btn("1", lambda: calc.click("1"), 4, 0, BTN)
btn("2", lambda: calc.click("2"), 4, 1, BTN)
btn("3", lambda: calc.click("3"), 4, 2, BTN)
btn("-", lambda: calc.click("-"), 4, 3, OP)

# Row 5
btn("0", lambda: calc.click("0"), 5, 0, BTN)
btn(".", lambda: calc.click("."), 5, 1, BTN)
btn("Ans", calc.use_ans, 5, 2, BTN)
btn("+", lambda: calc.click("+"), 5, 3, OP)

# Row 6
btn("sin", lambda: calc.func_click("sin"), 6, 0, BTN)
btn("cos", lambda: calc.func_click("cos"), 6, 1, BTN)
btn("tan", lambda: calc.func_click("tan"), 6, 2, BTN)
btn("=", calc.equal, 6, 3, OP)

# ---------------- RUN ----------------
root.mainloop()