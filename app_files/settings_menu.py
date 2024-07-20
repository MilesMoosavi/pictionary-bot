import tkinter as tk
from tkinter import filedialog
import json
import os
from capture_area import CaptureArea

class SettingsMenu:
    def __init__(self, master):
        self.master = master
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'config', 'settings.json')
        self.create_window()  # Initialize GUI elements first
        self.ensure_settings()

    def ensure_settings(self):
        if not os.path.exists(self.config_file):
            self.config = {
                'WordbankMethod': 'default',
                'CustomWordbankPath': '',
                'CaptureCoordinates': 'None',
                'LastPosition': '400x300+100+100'
            }
            self.save_settings()
        else:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)

            if 'WordbankMethod' not in self.config:
                self.config['WordbankMethod'] = 'default'
            if 'CustomWordbankPath' not in self.config:
                self.config['CustomWordbankPath'] = ''
            if 'CaptureCoordinates' not in self.config:
                self.config['CaptureCoordinates'] = 'None'
            if 'LastPosition' not in self.config:
                self.config['LastPosition'] = '400x300+100+100'
            self.save_settings()

        self.load_settings()

    def load_settings(self):
        self.wordbank_var.set(self.config.get('WordbankMethod', 'default'))
        self.custom_wordbank_entry.delete(0, tk.END)
        self.custom_wordbank_entry.insert(0, self.config.get('CustomWordbankPath', ''))
        self.update_coordinates_display()
        self.toggle_wordbank_fields()

    def save_settings(self):
        self.config['WordbankMethod'] = self.wordbank_var.get()
        self.config['CustomWordbankPath'] = self.custom_wordbank_entry.get()
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

    def create_window(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title('HintMaster Settings')
        self.settings_window.geometry('400x300')
        self.settings_window.withdraw()

        # Capture area configuration
        capture_area_button = tk.Button(self.settings_window, text="Select Capture Area", command=self.select_capture_area)
        capture_area_button.pack(pady=(10, 5))

        # Display configured coordinates
        self.capture_label = tk.Label(self.settings_window, text="Configured Coordinates: None")
        self.capture_label.pack(pady=(10, 10))

        # Wordbank method selection
        tk.Label(self.settings_window, text="Wordbank Method:").pack()
        self.wordbank_var = tk.StringVar(value="default")  # Initialize the variable here
        tk.Radiobutton(self.settings_window, text="Default (Use App's Built-In List of Words)", variable=self.wordbank_var, value="default", command=self.toggle_wordbank_fields).pack()
        tk.Radiobutton(self.settings_window, text="Custom", variable=self.wordbank_var, value="custom", command=self.toggle_wordbank_fields).pack()

        # Custom wordbank path and browse button
        custom_frame = tk.Frame(self.settings_window)
        custom_frame.pack(fill='x', pady=(0, 20))
        self.custom_wordbank_entry = tk.Entry(custom_frame)
        self.custom_wordbank_entry.pack(side='left', fill='x', expand=True)
        self.browse_button = tk.Button(custom_frame, text="Browse", command=self.browse_wordbank)
        self.browse_button.pack(side='left')

        return_button = tk.Button(self.settings_window, text="Return to Main Menu", command=self.hide)
        return_button.pack(side='right', pady=(10, 10))  # Position the button at the bottom right

    def toggle_wordbank_fields(self):
        if self.wordbank_var.get() == 'default':
            self.custom_wordbank_entry.config(state='disabled')
            self.browse_button.config(state='disabled')
        else:
            self.custom_wordbank_entry.config(state='normal')
            self.browse_button.config(state='normal')

    def select_capture_area(self):
        capture_area = CaptureArea(self.master, self)
        capture_area.show()

    def browse_wordbank(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.custom_wordbank_entry.delete(0, tk.END)
            self.custom_wordbank_entry.insert(0, filepath)
            self.config['CustomWordbankPath'] = filepath
            self.save_settings()

    def show(self):
        self.load_settings()  # Ensure settings are loaded each time the settings window is shown
        self.settings_window.deiconify()

    def hide(self):
        self.save_settings()
        self.settings_window.withdraw()

    def update_coordinates_display(self, x1=None, y1=None, x2=None, y2=None):
        if x1 and y1 and x2 and y2:
            self.config['CaptureCoordinates'] = f'({x1}, {y1}), ({x2}, {y2})'
            self.save_settings()
        capture_coordinates = self.config.get('CaptureCoordinates', 'None')
        self.capture_label.config(text=f"Configured Coordinates: {capture_coordinates}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsMenu(root)
    root.mainloop()