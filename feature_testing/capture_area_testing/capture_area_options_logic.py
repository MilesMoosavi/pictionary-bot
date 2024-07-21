import tkinter as tk
from tkinter import Toplevel, Canvas, ttk
import ctypes
import json
from win32gui import EnumWindows, GetWindowText, IsWindowVisible
from win32process import GetWindowThreadProcessId
import psutil
import os

# Set process DPI awareness
ctypes.windll.user32.SetProcessDPIAware()

def get_screen_scaling():
    hdc = ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
    ctypes.windll.user32.ReleaseDC(0, hdc)
    return dpi / 96

def list_windows():
    windows = []
    def callback(hwnd, extra):
        if IsWindowVisible(hwnd) and GetWindowText(hwnd):
            pid = GetWindowThreadProcessId(hwnd)[1]
            process_name = psutil.Process(pid).name()
            window_title = GetWindowText(hwnd)
            # Filter out unwanted windows
            if "Grammarly" not in window_title and window_title.strip() != "":
                windows.append(f"[{process_name}]: {window_title}")
    EnumWindows(callback, None)
    return windows

class CaptureArea:
    def __init__(self, master, settings_menu):
        self.master = master
        self.settings_menu = settings_menu

    def create_window(self):
        self.top = Toplevel(self.master, bg='black')
        self.top.attributes('-fullscreen', True)
        self.top.attributes('-alpha', 0.75)  # Make the window semi-transparent

        self.canvas = Canvas(self.top, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        self.top.bind('<Escape>', self.on_escape)  # Allow exiting with Escape key

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
        self.end_x = event.x
        self.end_y = event.y

        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        self.top.destroy()  # Close the window after selection

        # Update coordinates display in the GUI and print them
        self.settings_menu.update_coordinates_display(self.start_x, self.start_y, self.end_x, self.end_y)
        print(f"Selected area: ({self.start_x}, {self.start_y}), ({self.end_x}, {self.end_y})")

    def on_escape(self, event):
        print("Screen selection aborted by user.")
        self.top.destroy()

    def show(self):
        self.create_window()  # Ensure a new window is created each time

class SettingsMenu:
    def __init__(self, master):
        self.master = master
        self.scale_factor = get_screen_scaling()
        self.settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
        self.settings = self.load_settings()
        self.create_window()

    def create_window(self):
        self.master.title('Select Capture Area')
        scaled_width = int(500 * self.scale_factor)
        scaled_height = int(300 * self.scale_factor)
        self.master.geometry(f'{scaled_width}x{scaled_height}')

        # Capture area configuration
        capture_area_button = tk.Button(self.master, text="Select Capture Area", command=self.select_capture_area)
        capture_area_button.pack(pady=(10, 5))

        # Display configured coordinates
        self.capture_label = tk.Label(self.master, text="Configured Coordinates: None")
        self.capture_label.pack(pady=(10, 10))

        # Create frames for layout
        window_frame = tk.Frame(self.master)
        window_frame.pack(pady=(5, 5))
        priority_frame = tk.Frame(self.master)
        priority_frame.pack(pady=(5, 5))

        # Window selection label and combobox
        self.window_label = tk.Label(window_frame, text="Window: ")
        self.window_label.pack(side=tk.LEFT)
        self.window_combobox = ttk.Combobox(window_frame, postcommand=self.update_window_list, width=60)
        self.window_combobox.pack(side=tk.LEFT)

        # Window match priority label and combobox
        self.match_priority_label = tk.Label(priority_frame, text="Window Match Priority: ")
        self.match_priority_label.pack(side=tk.LEFT)
        self.match_priority_combobox = ttk.Combobox(priority_frame, values=["Match executable", "Match title"], state="readonly")
        self.match_priority_combobox.pack(side=tk.LEFT)
        self.match_priority_combobox.current(self.settings.get("match_priority", 0))
        self.match_priority_combobox.bind("<<ComboboxSelected>>", self.update_window_selection)

        # Load saved window and match priority
        self.window_combobox.set(self.settings.get("selected_window", ""))
        self.update_window_selection(None)

        # Load and display saved capture coordinates
        capture_coordinates = self.settings.get("CaptureCoordinates", None)
        if capture_coordinates:
            self.update_coordinates_display(*capture_coordinates)

    def select_capture_area(self):
        capture_area = CaptureArea(self.master, self)
        capture_area.show()

    def update_coordinates_display(self, x1, y1, x2, y2):
        capture_coordinates = (x1, y1, x2, y2)
        self.capture_label.config(text=f"Configured Coordinates: {capture_coordinates}")
        self.settings['CaptureCoordinates'] = capture_coordinates
        self.save_settings()

    def update_window_list(self):
        windows = list_windows()
        current_priority = self.match_priority_combobox.get()
        if current_priority == "Match executable":
            self.window_combobox['values'] = windows
        elif current_priority == "Match title":
            self.window_combobox['values'] = [win.split(": ")[1] for win in windows]

    def update_window_selection(self, event):
        current_value = self.window_combobox.get()
        self.update_window_list()
        if current_value:
            if self.match_priority_combobox.get() == "Match executable":
                for win in list_windows():
                    if current_value in win:
                        self.window_combobox.set(win)
                        break
            else:
                self.window_combobox.set(current_value.split(": ")[-1])
        self.save_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                # Ensure coordinates are loaded as a tuple of integers
                if "CaptureCoordinates" in settings:
                    coordinates_str = settings["CaptureCoordinates"].replace("(", "").replace(")", "")
                    settings["CaptureCoordinates"] = tuple(map(int, coordinates_str.split(',')))
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_settings(self):
        settings = {
            "selected_window": self.window_combobox.get(),
            "match_priority": self.match_priority_combobox.current(),
            "CaptureCoordinates": ','.join(map(str, self.settings.get("CaptureCoordinates", ())))
        }
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsMenu(root)
    root.mainloop()