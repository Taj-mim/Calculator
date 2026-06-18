import tkinter as tk

def click(num):
   display.insert(tk.END,num)

def equal():
    try:
        result=eval(display.get())
        display.delete(0,tk.END)
        display.insert(0,str(result))
    except:
        display.delete(0,tk.END)
        display.insert(0,"error") 

def clear():
    display.delete(0,tk.END)

window=tk.Tk()
window.title("SCIENTIFIC CALCULATOR")
window.geometry("450x450")
display=tk.Entry(window,font=("Time New Roman",15),justify="right",bd=9)
display.grid(row=0, column=0, columnspan=5, ipadx=100, ipady=8)
tk.Button(window, text="1", command=lambda: click("1")).grid(row=1, column=0)
tk.Button(window, text="2", command=lambda: click("2")).grid(row=1, column=1)
tk.Button(window, text="3", command=lambda: click("3")).grid(row=1, column=2)
tk.Button(window, text="/", command=lambda: click("/")).grid(row=1, column=3)

tk.Button(window, text="4", command=lambda: click("4")).grid(row=2, column=0)
tk.Button(window, text="5", command=lambda: click("5")).grid(row=2, column=1)
tk.Button(window, text="6", command=lambda: click("6")).grid(row=2, column=2)
tk.Button(window, text="*", command=lambda: click("*")).grid(row=2, column=3)

tk.Button(window, text="7", command=lambda: click("7")).grid(row=3, column=0)
tk.Button(window, text="8", command=lambda: click("8")).grid(row=3, column=1)
tk.Button(window, text="9", command=lambda: click("9")).grid(row=3, column=2)
tk.Button(window, text="-", command=lambda: click("-")).grid(row=3, column=3)

tk.Button(window, text="0", command=lambda: click("0")).grid(row=4, column=0)
tk.Button(window, text="C", command=clear).grid(row=4, column=1)
tk.Button(window, text="=", command=equal).grid(row=4, column=2)
tk.Button(window, text="+", command=lambda: click("+")).grid(row=4, column=3)
window.mainloop()