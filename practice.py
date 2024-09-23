import tkinter as tk
from tkinter import ttk, RAISED

root = tk.Tk()
root.title("Practice Game - Let's see how beautiful I can make this page")
root.geometry('700x400')
root['bg'] = 'skyblue'
root.resizable(False, False)
light_purple = '#E6E6FA'
# Left frame
left_frame = tk.Frame(root, width=250, height=200, bg='skyblue')
left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
left_frame.grid_propagate(False)  # Prevent left_frame from shrinking to fit its children

# Right frame
right_frame = tk.Frame(root, width=650, height=200, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

# Load and display the image
image = tk.PhotoImage(file="calculus.png")
label = tk.Label(right_frame, image=image)

label.pack(expand=True)

# Tool bar in the left frame
tool_bar = tk.Frame(left_frame, width=180, height=185, bg='pink')
tool_bar.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
tool_bar.grid_propagate(False)  # Prevent tool_bar from shrinking to fit its children

# Label in the tool bar
levels_label = tk.Label(tool_bar, text="Levels", relief=RAISED, font=("Times New Roman", 14, "bold"))
levels_label.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)

welcome_label = tk.Label(left_frame, text="Welcome To The Calculus Game", relief=tk.RAISED, font=("Times New Roman", 16, "italic"), wraplength=275, justify="center", bg = 'skyblue')
welcome_label.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()


