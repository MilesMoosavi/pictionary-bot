import os
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import subprocess
import sys
from ocr_utils import detect_underscores_and_letters

# Initialize flag
annotations_made = False

# Function to run OCR using the custom OCR utility
def run_ocr():
    global annotations_made
    img_label.config(text="Processing...")
    root.update_idletasks()
    image_path = file_entry.get()
    detected_elements, recognized_text, result_image_path, preprocessed_image_path, original_image_path = detect_underscores_and_letters(image_path)
    
    # Update GUI with decoded text
    decoded_text_box.delete(1.0, tk.END)
    decoded_text_box.insert(tk.END, recognized_text)
    
    # Load and display the original image
    original_img = Image.open(original_image_path)
    original_img.thumbnail((600, 400))  # Resize image
    original_img = ImageTk.PhotoImage(original_img)
    img_display.config(image=original_img)
    img_display.image = original_img
    
    # Load and display the preprocessed image
    preprocessed_img = Image.open(preprocessed_image_path)
    preprocessed_img.thumbnail((600, 400))  # Resize image
    preprocessed_img = ImageTk.PhotoImage(preprocessed_img)
    img_label.config(image=preprocessed_img)
    img_label.image = preprocessed_img
    
    # Load and display the image with annotations
    result_img = Image.open(result_image_path)
    result_img.thumbnail((600, 400))  # Resize image
    result_img = ImageTk.PhotoImage(result_img)
    img_label.config(image=result_img)
    img_label.image = result_img
    
    # Display the confidence levels in a label
    conf_text = "\n".join([f"Character: {elem[4]}, Confidence: {int(elem[5])}%" for elem in detected_elements])
    conf_label.config(text=conf_text)

    img_label.config(text="Result:")

    # Update the flag and enable the clear button
    annotations_made = True
    clear_button.config(state=tk.NORMAL)

def load_image(image_path):
    return Image.open(image_path)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        update_image_path(file_path)

def paste_from_clipboard():
    try:
        image = ImageGrab.grabclipboard()
        if image:
            src_dir = os.path.join(os.path.dirname(__file__), "src")
            if not os.path.exists(src_dir):
                os.makedirs(src_dir)
            image_path = os.path.join(src_dir, "clipboard_image.png")
            image.save(image_path)
            update_image_path(image_path)
    except Exception as e:
        print("Failed to paste image from clipboard:", str(e))

def update_image_path(file_path):
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    with open(json_path, 'w') as f:
        json.dump({"image_path": file_path}, f)
    load_preview_image(file_path)

def load_preview_image(image_path):
    global annotations_made
    try:
        img = load_image(image_path)
        img.thumbnail((600, 400))
        img = ImageTk.PhotoImage(img)
        img_display.config(image=img)
        img_display.image = img
        img_label.config(text=f"Uploaded image: {os.path.basename(image_path)}")
        run_ocr_button.config(state=tk.NORMAL)
        # Disable the clear button since no annotations are made yet
        annotations_made = False
        clear_button.config(state=tk.DISABLED)
    except FileNotFoundError:
        img_display.config(image='')
        img_label.config(text="Uploaded image: None")
        run_ocr_button.config(state=tk.DISABLED)
        clear_button.config(state=tk.DISABLED)

def reload_script():
    root.destroy()
    subprocess.Popen([sys.executable, os.path.abspath(__file__)])

def clear_annotations():
    image_path = file_entry.get()
    if image_path:
        load_preview_image(image_path)

def paste_clipboard_shortcut(event):
    paste_from_clipboard()

# GUI setup
root = tk.Tk()
root.title("PytesseractOCR")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

button_frame = tk.Frame(frame)
button_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

file_entry = tk.Entry(button_frame, width=60)
file_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

browse_button = tk.Button(button_frame, text="↑", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=5, pady=5)

paste_button = tk.Button(button_frame, text="📋", command=paste_from_clipboard)
paste_button.pack(side=tk.LEFT, padx=5, pady=5)

run_ocr_button = tk.Button(button_frame, text="Run OCR", state=tk.DISABLED, command=run_ocr)
run_ocr_button.pack(side=tk.LEFT, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear Annotations", command=clear_annotations, state=tk.DISABLED)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

reload_button = tk.Button(button_frame, text="⟳", command=reload_script)
reload_button.pack(side=tk.LEFT, padx=5, pady=5)

img_label = tk.Label(frame, text="Uploaded image: None", anchor="center")
img_label.grid(row=0, column=1, columnspan=2, pady=5)

img_display = tk.Label(frame)
img_display.grid(row=1, column=1, padx=10, pady=10)

decoded_text_box = tk.Text(frame, height=20, width=60)
decoded_text_box.grid(row=1, column=2, padx=5, pady=5)

conf_label = tk.Label(frame, text="", justify=tk.LEFT)
conf_label.grid(row=1, column=3, padx=5, pady=5)

json_path = os.path.join(os.path.dirname(__file__), "settings.json")
if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        settings = json.load(f)
        if "image_path" in settings:
            file_entry.insert(0, settings["image_path"])
            load_preview_image(settings["image_path"])

# Bind Ctrl+V to paste from clipboard
root.bind('<Control-v>', paste_clipboard_shortcut)

root.mainloop()