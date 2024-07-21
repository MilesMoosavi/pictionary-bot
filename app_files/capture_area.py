import tkinter as tk
import json
import os

class CaptureArea:
    def __init__(self, master, settings):
        self.master = master
        self.settings = settings  # Pass the settings object for configuration access

    def create_window(self):
        self.top = tk.Toplevel(self.master, bg='black')
        self.top.attributes('-fullscreen', True)
        self.top.attributes('-alpha', 0.75)  # Make the window semi-transparent

        self.canvas = tk.Canvas(self.top, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        self.top.bind('<Escape>', lambda e: self.top.destroy())  # Allow exiting with Escape key

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = None

    def on_mouse_drag(self, event):
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red', fill='gray', width=2)
        else:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        self.top.destroy()  # Close the window after selection

        # Save and update the settings with the new coordinates
        self.save_capture_area(self.start_x, self.start_y, self.end_x, self.end_y)
        self.settings.update_coordinates_display(self.start_x, self.start_y, self.end_x, self.end_y)

    def save_capture_area(self, x1, y1, x2, y2):
        self.settings.config['CaptureCoordinates'] = f'({x1}, {y1}), ({x2}, {y2})'
        with open(self.settings.config_file, 'w') as file:
            json.dump(self.settings.config, file, indent=4)

    def show(self):
        self.create_window()  # Ensure a new window is created each time

    def close(self):
        if self.top:
            self.top.destroy()