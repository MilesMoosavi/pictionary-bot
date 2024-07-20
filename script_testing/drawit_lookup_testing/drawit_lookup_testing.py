import sys
import tkinter as tk
from tkinter import StringVar, Listbox, Scrollbar, Toplevel, Checkbutton, IntVar, Label
import re
import os
import json

# Get the base directory
if getattr(sys, 'frozen', False):
    # Running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # Running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the folder containing the word list files
word_list_folder = os.path.join(script_dir, 'wordlists')

# Define the path to the user added words file
user_added_words_file = os.path.join(word_list_folder, 'user_added_words.txt')

# Define the path to the JSON file for saving settings
settings_file = os.path.join(script_dir, 'settings.json')

# Initialize global word set and recent changes list
word_set = set()
recent_changes = []

# Initialize global index for listbox navigation
current_index = 0

# Function to read word lists from selected files
def read_word_lists(selected_files):
    global word_set
    word_set = set()
    for filename in selected_files:
        file_path = os.path.join(word_list_folder, filename)
        with open(file_path, 'r') as file:
            word_set.update([line.strip().lower() for line in file])
    return sorted(list(word_set))

# Function to load settings from JSON file
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
            return settings
    return None

# Function to save all settings to JSON file
def save_settings():
    position = root.geometry().split('+')[1:]
    settings = {
        'x': position[0],
        'y': position[1],
        'always_on_top': on_top_var.get(),
        'user_selections': selected_files,
        'recent_changes': recent_changes
    }
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

# Function to update Listbox height
def update_listbox_height(event):
    window_height = root.winfo_height()
    listbox_height = (window_height - 170) // 20  # Adjust the height calculation as needed
    listbox.config(height=listbox_height)

# Function to update input length label
def update_input_length(*args):
    length = len(entry_var.get())
    if length == 0:
        input_length_label.config(text="")
    else:
        input_length_label.config(text=str(length))

# Read all available word list files
available_files = [filename for filename in os.listdir(word_list_folder) if filename.endswith('.txt')]

# Create main window
root = tk.Tk()
root.geometry("500x200")
root.title("Word Matcher")

# Load settings
settings = load_settings()
if settings:
    root.geometry(f"+{settings['x']}+{settings['y']}")
    on_top_var = IntVar(value=settings['always_on_top'])
    root.attributes('-topmost', settings['always_on_top'])
    selected_files = settings['user_selections']
    recent_changes = settings['recent_changes']
else:
    on_top_var = IntVar(value=1)
    selected_files = available_files.copy()
    recent_changes = []

# Ensure the window's "Always on Top" state matches the loaded settings
root.attributes('-topmost', on_top_var.get())

# Bring the window to the front once on load
root.lift()
root.after(10, lambda: root.lift())

word_list = read_word_lists(selected_files)

def update_listbox(word_fragment):
    global current_index
    current_index = 0  # Reset index on new input
    listbox.delete(0, tk.END)
    
    if "_" in word_fragment:
        regex_str = "^"

        for char in word_fragment:
            if char == "_":
                regex_str += "\\w"
            elif char in [".", "/"]:
                regex_str += "\\" + char
            else:
                regex_str += char

        regex_str += "$"

        regex = re.compile(regex_str, re.IGNORECASE)
        possible_words = [word for word in word_list if regex.match(word)]
    else:
        possible_words = [word for word in word_list if word.startswith(word_fragment)]
    
    for word in possible_words:
        listbox.insert(tk.END, word)
    
    if possible_words:
        listbox.select_set(current_index)
        listbox.activate(current_index)

    update_selection_label()

def on_key_release(event):
    if event.keysym not in ("Up", "Down"):
        typed_word = entry_var.get().lower()
        update_listbox(typed_word)

def flash_entry():
    entry.config({"background": "red"})
    root.after(100, lambda: entry.config({"background": "white"}))
    root.after(200, lambda: entry.config({"background": "red"}))
    root.after(300, lambda: entry.config({"background": "white"}))

def add_to_recent_changes(action, word):
    recent_changes.append({"action": action, "word": word})
    if len(recent_changes) > 10:
        recent_changes.pop(0)
    save_settings()
    update_recent_changes_window()

def add_word(event=None):
    global word_set, word_list
    word = entry_var.get().strip().lower()
    if word:
        if word not in word_set:
            with open(user_added_words_file, 'a') as file:
                file.write(word + '\n')
            word_set.add(word)
            word_list.append(word)
            word_list.sort()
            update_listbox(entry_var.get().lower())
            add_to_recent_changes("+", word)
        else:
            flash_entry()
    entry_var.set("")

def remove_word():
    global word_set, word_list
    word = entry_var.get().strip().lower()
    if word:
        if word in word_set:
            word_set.remove(word)
            word_list.remove(word)
            with open(user_added_words_file, 'w') as file:
                for w in word_set:
                    file.write(w + '\n')
            update_listbox(entry_var.get().lower())
            add_to_recent_changes("-", word)
        else:
            flash_entry()
    entry_var.set("")

def show_recent_changes():
    global recent_window, listbox_left, listbox_right
    recent_window = Toplevel(root)
    recent_window.title("Recent Changes")
    recent_window.attributes('-topmost', True)
    
    frame_left = tk.Frame(recent_window)
    frame_left.pack(side="left", fill="both", expand=True)
    
    frame_right = tk.Frame(recent_window)
    frame_right.pack(side="right", fill="both", expand=True)
    
    scrollbar_left = Scrollbar(frame_left)
    scrollbar_left.pack(side="right", fill="y")
    
    listbox_left = Listbox(frame_left, yscrollcommand=scrollbar_left.set, width=5)
    listbox_left.pack(side="left", fill="both", expand=True)
    scrollbar_left.config(command=listbox_left.yview)
    
    scrollbar_right = Scrollbar(frame_right)
    scrollbar_right.pack(side="right", fill="y")
    
    listbox_right = Listbox(frame_right, yscrollcommand=scrollbar_right.set, width=30)
    listbox_right.pack(side="left", fill="both", expand=True)
    scrollbar_right.config(command=listbox_right.yview)
    
    update_recent_changes_window()

    # Ensure the recent window stays on top
    root.after(10, lambda: recent_window.attributes('-topmost', True))

def update_recent_changes_window():
    if recent_window and listbox_left and listbox_right:
        listbox_left.delete(0, tk.END)
        listbox_right.delete(0, tk.END)
        for change in recent_changes:
            listbox_left.insert(tk.END, change["action"])
            listbox_right.insert(tk.END, change["word"])

def show_wordlist_selection():
    def update_selected_files():
        global selected_files, word_list
        selected_files = [available_files[i] for i, var in enumerate(check_vars) if var.get() == 1]
        save_settings()
        word_list = read_word_lists(selected_files)
        update_listbox(entry_var.get().lower())
        selection_window.destroy()

    selection_window = Toplevel(root)
    selection_window.title("Select Word Lists")
    selection_window.attributes('-topmost', True)

    check_vars = [IntVar(value=1 if file in selected_files else 0) for file in available_files]

    for i, file in enumerate(available_files):
        chk = Checkbutton(selection_window, text=file, variable=check_vars[i])
        chk.pack(anchor='w')

    confirm_button = tk.Button(selection_window, text="Confirm", command=update_selected_files)
    confirm_button.pack(pady=10)

    # Ensure the selection window stays on top
    root.after(10, lambda: selection_window.attributes('-topmost', True))

def on_listbox_select(event):
    selected_word = listbox.get(listbox.curselection())
    entry_var.set(selected_word)
    update_selection_label()

def toggle_on_top():
    root.attributes('-topmost', on_top_var.get())
    save_settings()

def on_arrow_key(event):
    global current_index
    if event.keysym == "Down":
        if current_index < listbox.size() - 1:
            current_index += 1
            listbox.select_clear(0, tk.END)
            listbox.select_set(current_index)
            listbox.activate(current_index)
            listbox.see(current_index)
    elif event.keysym == "Up":
        if current_index > 0:
            current_index -= 1
            listbox.select_clear(0, tk.END)
            listbox.select_set(current_index)
            listbox.activate(current_index)
            listbox.see(current_index)
    update_selection_label()

def select_from_listbox(event):
    if listbox.curselection():
        selected_word = listbox.get(listbox.curselection())
        entry_var.set(selected_word)

def copy_to_clipboard(event):
    try:
        selected_word = listbox.get(listbox.curselection())
        root.clipboard_clear()
        root.clipboard_append(selected_word)
    except:
        pass

def select_all(event):
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')
    return 'break'

def update_selection_label():
    if listbox.curselection():
        selected_index = listbox.curselection()[0] + 1
        total_items = listbox.size()
        selection_label_var.set(f"Selected {selected_index} of {total_items} items")

# Create and place widgets
frame_top = tk.Frame(root)
frame_top.pack(pady=5, anchor='w')

select_button = tk.Button(frame_top, text="Select Word Lists", command=show_wordlist_selection)
select_button.pack(side=tk.LEFT, padx=5)

recent_changes_button = tk.Button(frame_top, text="Recent Changes", command=show_recent_changes)
recent_changes_button.pack(side=tk.LEFT, padx=5)

on_top_checkbox = tk.Checkbutton(frame_top, text="Always on Top", variable=on_top_var, command=toggle_on_top)
on_top_checkbox.pack(side=tk.RIGHT, padx=5)

frame_entry = tk.Frame(root)
frame_entry.pack(pady=5)

entry_label = tk.Label(frame_entry, text="Enter obfuscated word:")
entry_label.pack(side=tk.LEFT, padx=5)

entry_var = StringVar()
entry_var.trace_add("write", update_input_length)
entry = tk.Entry(frame_entry, textvariable=entry_var, width=40)
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<KeyRelease>", on_key_release)
entry.bind("<Return>", add_word)
entry.bind("<Down>", on_arrow_key)
entry.bind("<Up>", on_arrow_key)

input_length_label = Label(frame_entry, text="", width=2, anchor='w')
input_length_label.pack(side=tk.LEFT)

add_button = tk.Button(frame_entry, text="+", command=add_word, width=3)
add_button.pack(side=tk.LEFT, padx=2)

remove_button = tk.Button(frame_entry, text="-", command=remove_word, width=3)
remove_button.pack(side=tk.LEFT, padx=2)

# Listbox and Scrollbar for possible words
frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=5, fill='both', expand=True)

scrollbar = Scrollbar(frame_bottom, orient="vertical")
scrollbar.pack(side="right", fill="y")

listbox = Listbox(frame_bottom, width=50, height=5, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)
listbox.bind('<<ListboxSelect>>', on_listbox_select)
listbox.bind("<Return>", select_from_listbox)

# Label to display the selection info
selection_label_var = StringVar()
selection_label = tk.Label(root, textvariable=selection_label_var, anchor='w')
selection_label.pack(side="left", fill="x", padx=5, pady=5)
selection_label_var.set("Selected 0 of 0 items")

# Initialize listbox with all words
update_listbox("")

# Set initial state of the window on top
root.attributes('-topmost', on_top_var.get())

# Bring the window to the front once on load
root.lift()
root.after(10, lambda: root.lift())

# Bind the window move event
root.bind('<Configure>', lambda event: save_settings() if event.widget == root else None)
root.bind('<Configure>', update_listbox_height)

# Initialize recent window variables
recent_window = None
listbox_left = None
listbox_right = None

# Run the application
root.mainloop()