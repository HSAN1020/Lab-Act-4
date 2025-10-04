import tkinter as tk
from tkinter import filedialog

def pick_text_file():
    path = filedialog.askopenfilename(
        title="Select a text file",
        initialdir=".",
        filetypes=[
            ("Text files", "*.txt *.md *.log *.csv"),
            ("All files", "*.*"),
        ],
    )
    if path:
        selected_var.set(path)       
        print(path)                 
        root.clipboard_clear()       
        root.clipboard_append(path)
    else:
        selected_var.set("No file selected")

# --- UI setup ---
root = tk.Tk()
root.title("Get Text File Name")

selected_var = tk.StringVar(value="No file selected")

tk.Label(root, text="Selected file:").pack(padx=10, pady=(10, 0), anchor="w")
tk.Entry(root, textvariable=selected_var, width=60).pack(padx=10, pady=5, fill="x")
tk.Button(root, text="Browse…", command=pick_text_file).pack(padx=10, pady=(0,10), anchor="w")
tk.Button(root, text="Quit", command=root.destroy).pack(padx=10, pady=(0,10), anchor="e")

root.mainloop()
