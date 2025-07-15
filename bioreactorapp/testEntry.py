import tkinter as tk
root = tk.Tk()

val="1"
value=tk.StringVar()
value.set(val)

def updateVal():
    if entry.get():
        try:
            if len(entry.get())==0: ##null entry?
                pwv=0
            elif float(entry.get()) > 100: ##max 100 percent
                pwv=4095
            else:
                pwv=round(int(float(entry.get()))*40.95)  ##Round var and scale to 0-4095
        except ValueError:
            tk.messagebox.showerror(title='Not a number', message='Please only numbers')
            value.set("0")
            
    root.after(1000, updateVal)
    
def only_numbers(char):
    return char.isdigit()
validation = root.register(only_numbers)


entry=tk.Entry(root, textvariable=value, validate="key", validatecommand=(validation,'%S'))
entry.pack()

root.after(1000, updateVal)
root.mainloop()