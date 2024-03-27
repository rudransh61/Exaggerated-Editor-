import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
from tkinter import ttk
import subprocess

def open_file(event=None):
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())
            display_files_in_directory()

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.get(1.0, tk.END))

def highlight_cursor(event):
    global last_index, position_x, position_y
    cursor_index = float(editor.index(tk.INSERT))
    editor.tag_add("cursor", cursor_index)

    current_line, current_col = map(int, editor.index(tk.INSERT).split('.'))
    if last_index:
        last_line, last_col = map(int, last_index.split('.'))

        # Move frame down when cursor moves up
        if current_line < last_line:
            position_y += 5
        # Move frame up when cursor moves down
        elif current_line > last_line:
            position_y -= 5

        # Move frame right when cursor moves left
        if current_col < last_col:
            position_x += 5
        # Move frame left when cursor moves right
        elif current_col > last_col:
            position_x -= 5

    if editor.get(f"{current_line}.0", f"{current_line}.end-1c") == "":
        position_x = 15

    editor_frame.place(x=position_x * 10, y=position_y * 16)

    last_index = editor.index(tk.INSERT)

def copy_text(event=None):
    editor.clipboard_clear()
    editor.clipboard_append(editor.selection_get())

def cut_text(event=None):
    copy_text()
    editor.delete("sel.first", "sel.last")

def paste_text(event=None):
    editor.insert(tk.INSERT, editor.clipboard_get())

def change_text_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    color = "#%02x%02x%02x" % (r, g, b)
    editor.config(fg=color)
    root.after(100, change_text_color)

def insert_tab(event):
    editor.insert(tk.INSERT, " " * 4)
    return 'break'

def display_files_in_directory():
    global file_path
    directory = os.path.dirname(file_path)
    if directory:
        files = os.listdir(directory)
        if files:
            file_list_window = tk.Toplevel(root)
            file_list_window.title("Files in Directory")
            file_list_window.geometry("400x300")

            file_list_label = tk.Label(file_list_window, text="Files in Directory:")
            file_list_label.pack()

            file_listbox = tk.Listbox(file_list_window)
            for file in files:
                file_listbox.insert(tk.END, file)
            file_listbox.pack(fill="both", expand=True)
        else:
            messagebox.showinfo("No Files", "No files found in the directory.")
    else:
        messagebox.showinfo("No Folder Selected", "Please open a file first to display its directory.")

def open_terminal():
    subprocess.Popen(['powershell'])

position_x = 15
position_y = 5
last_index = None
file_path = None

root = tk.Tk()
root.title("ExaggeratedEditing")
root.configure(background='black')
root.geometry("800x500")

style = ttk.Style()
style.configure("Custom.TFrame", background="black")

editor_frame = ttk.Frame(root, style="Custom.TFrame")
editor_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

editor = tk.Text(editor_frame, bg="#222", fg="#fff", font=("Courier", 60), wrap="none", insertbackground="red")
editor.pack(side="left", fill="both", expand=True)

root.bind("<Control-1>", lambda event: display_files_in_directory())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-c>", lambda event: copy_text())
root.bind("<Control-x>", lambda event: cut_text())
root.bind("<Control-v>", lambda event: paste_text())
editor.bind("<Tab>", insert_tab)

root.bind("<Control-t>", lambda event: open_terminal())  # Ctrl+T to open terminal

editor.bind("<Key>", highlight_cursor)

highlight_cursor(None)

change_text_color()

editor_frame.place(x=position_x * 10, y=position_y * 16)

root.mainloop()
