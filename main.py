import tkinter as tk
from tkinter import filedialog
import random
from tkinter import ttk

def open_file(event=None):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.get(1.0, tk.END))

# Function to highlight cursor
def highlight_cursor(event):
    global last_index, position_x, position_y
    cursor_index = float(editor.index(tk.INSERT))
    editor.tag_add("cursor", cursor_index)

    current_line, current_col = map(int, editor.index(tk.INSERT).split('.'))
    if last_index:
        last_line, last_col = map(int, last_index.split('.'))

        # Move frame down when cursor moves up
        if current_line < last_line:
            position_y += 1
        # Move frame up when cursor moves down
        elif current_line > last_line:
            position_y -= 1

        # Move frame right when cursor moves left
        if current_col < last_col:
            position_x += 1
        # Move frame left when cursor moves right
        elif current_col > last_col:
            position_x -= 1

    # Reset position_x when hitting an empty line
    if editor.get(f"{current_line}.0", f"{current_line}.end-1c") == "":
        position_x = 15

    editor_frame.place(x=position_x * 10, y=position_y * 16)  # Adjust according to your font and layout

    last_index = editor.index(tk.INSERT)

# Function to copy selected text
def copy_text(event=None):
    editor.clipboard_clear()
    editor.clipboard_append(editor.selection_get())

# Function to cut selected text
def cut_text(event=None):
    copy_text()
    editor.delete("sel.first", "sel.last")

# Function to paste copied/cut text
def paste_text(event=None):
    editor.insert(tk.INSERT, editor.clipboard_get())

# Function to change text color with RGB effect
def change_text_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    color = "#%02x%02x%02x" % (r, g, b)
    editor.config(fg=color)
    root.after(100, change_text_color)  # Change color every 100 milliseconds

# Function to handle tab insertion
def insert_tab(event):
    editor.insert(tk.INSERT, " " * 4)
    return 'break'  # Prevent default behavior

# Initialize position and last_index
position_x = 15
position_y = 5
last_index = None

# Create the main window
root = tk.Tk()
root.title("ExaggeratedEditing")
root.configure(background='black')
root.geometry("800x500")


# Create a custom style for the frame with a black background
style = ttk.Style()
style.configure("Custom.TFrame", background="black")

# Create a styled frame for the editor
editor_frame = ttk.Frame(root, style="Custom.TFrame")
editor_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Add padding here

# Create the editor with a font size of 60
editor = tk.Text(editor_frame, bg="#222", fg="#fff", font=("Courier", 60), wrap="none", insertbackground="red")
editor.pack(side="left", fill="both", expand=True)

# Bind keyboard shortcuts
root.bind("<Control-o>", lambda event: open_file())  # Ctrl+O to open file
root.bind("<Control-s>", lambda event: save_file())  # Ctrl+S to save file
root.bind("<Control-c>", lambda event: copy_text())  # Ctrl+C to copy
root.bind("<Control-x>", lambda event: cut_text())   # Ctrl+X to cut
root.bind("<Control-v>", lambda event: paste_text()) # Ctrl+V to paste
editor.bind("<Tab>", insert_tab)  # Tab key to insert 4 spaces

# Bind cursor movement event
editor.bind("<Key>", highlight_cursor)

# Highlight cursor
highlight_cursor(None)

# Start the RGB effect
change_text_color()

# Set the initial position of the editor frame
editor_frame.place(x=position_x * 10, y=position_y * 16)

root.mainloop()
