from ast import expr
from pydoc import text
import tkinter as tk
import math
from unicodedata import name
from unittest import result

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
        self.root.bind("<Key>", self.key_input)

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
            row=0, column=0,
            columnspan=4,
            sticky="nsew",
            ipadx=10, ipady=25,
            padx=10, pady=10
        )

    # ---------------- INPUT ----------------
    def click(self, value):
        if self.reset_next and value in "0123456789(":
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

    # ---------------- CALC ----------------
    def equal(self):
        try:
            expr = self.display.get().strip()
            if not expr:
                return

            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")

            open_brackets = expr.count("(")
            close_brackets = expr.count(")")
            expr += ")" * (open_brackets - close_brackets)

            result = eval(expr, {"__builtins__": {}, "math": math})

            if abs(result) < 1e-10:
                result = 0

            result = round(result, 10)

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            self.ans = result
            self.reset_next = True

        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "error")
            self.reset_next = True

    # ---------------- KEYBOARD ----------------
    def key_input(self, event):
        key = event.char

        if key in "0123456789+-*/().":
            self.click(key)

        elif event.keysym == "Return":
            self.equal()

        elif event.keysym == "BackSpace":
            self.delete_one()

    # ---------------- COPY ----------------
    def copy_result(self):
        result = self.display.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(result)

    # ---------------- VOICE ----------------
    def voice_input(self):
        import speech_recognition as sr
        import threading

        def listen():
            r = sr.Recognizer()

            with sr.Microphone() as source:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Listening...")

                audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                text = text.lower()

                text = text.replace("times", "*")
                text = text.replace("into", "*")
                text = text.replace("plus", "+")
                text = text.replace("minus", "-")
                text = text.replace("divided by", "/")

                text = text.replace("equal", "")
                text = text.replace("equals", "")

                text = text.strip()

                self.display.delete(0, tk.END)
                self.display.insert(0, text)

                self.equal()

            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "voice error")

        threading.Thread(target=listen, daemon=True).start()
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
        if self.reset_next and value in "0123456789(":
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
            expr = self.display.get().strip()
            if not expr:
                        return

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
def animate_click(button, cmd):
    button.config(relief="sunken")
    button.after(100, lambda: button.config(relief="flat"))

    if cmd:
        cmd()


def btn(text, cmd, r, c, color):
    button = tk.Button(
        root,
        text=text,
        bg=color,
        fg="#000000" if color != OP else "white",
        activebackground=BTN_HOVER,
        bd=0,
        relief="flat",
        font=("Arial", 14, "bold"),
        cursor="hand2"
    )

    button.config(
        command=lambda: animate_click(button, cmd)
    )

    button.grid(
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
btn("📋", calc.copy_result, 1, 2, BTN)
btn("🎤", calc.voice_input, 1, 3, BTN)

# Row 2
btn("(", lambda: calc.click("("), 2, 0, BTN)
btn(")", lambda: calc.click(")"), 2, 1, BTN)
btn("sin", lambda: calc.func_click("sin"), 2, 2, BTN)
btn("cos", lambda: calc.func_click("cos"), 2, 3, BTN)

# Row 3
btn("7", lambda: calc.click("7"), 3, 0, BTN)
btn("8", lambda: calc.click("8"), 3, 1, BTN)
btn("9", lambda: calc.click("9"), 3, 2, BTN)
btn("/", lambda: calc.click("/"), 3, 3, OP)

# Row 4
btn("4", lambda: calc.click("4"), 4, 0, BTN)
btn("5", lambda: calc.click("5"), 4, 1, BTN)
btn("6", lambda: calc.click("6"), 4, 2, BTN)
btn("*", lambda: calc.click("*"), 4, 3, OP)

# Row 5
btn("1", lambda: calc.click("1"), 5, 0, BTN)
btn("2", lambda: calc.click("2"), 5, 1, BTN)
btn("3", lambda: calc.click("3"), 5, 2, BTN)
btn("-", lambda: calc.click("-"), 5, 3, OP)

# Row 6
btn("0", lambda: calc.click("0"), 6, 0, BTN)
btn(".", lambda: calc.click("."), 6, 1, BTN)
btn("Ans", calc.use_ans, 6, 2, BTN)
btn("+", lambda: calc.click("+"), 6, 3, OP)
#Row 7
btn("tan", lambda: calc.func_click("tan"), 7, 0, BTN)
btn("=", calc.equal, 7, 3, OP)

# ---------------- RUN ----------------
root.mainloop()