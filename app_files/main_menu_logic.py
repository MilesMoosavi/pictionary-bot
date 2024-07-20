import tkinter as tk
from tkinter import messagebox
import threading
import time
from settings_menu import SettingsMenu
from capture_logic import CaptureLogic
import os
import sys
import configparser

class MainMenuLogic:
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root

        # Load settings
        self.config = configparser.ConfigParser()
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'settings.ini')
        self.load_settings()

        self.capture_logic = CaptureLogic(self.update_display)  # Correctly pass the update_display as a callback

        self.capturing = False
        self.settings_menu = SettingsMenu(self.root)

        # Set window position and size based on last saved position
        self.root.geometry(self.config['Settings'].get('LastPosition', '400x200+100+100'))
        self.root.after(0, self.root.focus_force)

        # Display saved coordinates if they exist
        self.update_coordinates_display()

    def load_settings(self):
        print("Loading settings...")

        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        if 'Settings' not in self.config:
            self.config['Settings'] = {
                'LastPosition': '400x200+100+100',
                'CaptureCoordinates': 'None'
            }

        print("Settings loaded.\n")

    def save_settings(self):
        print("Saving settings...")

        self.config['Settings']['LastPosition'] = self.root.geometry()
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

        print("Settings saved.\n")

    def toggle_capture(self):
        if self.capturing:
            self.capture_logic.stop_capture()
            self.gui.label_status.config(text='Capture not in session')
            self.clear_text_display()
        else:
            threading.Thread(target=self.simulate_capture).start()
            self.gui.label_status.config(text='Looking for hint to capture...')
            self.clear_text_display()
        self.capturing = not self.capturing

    def simulate_capture(self):
        time.sleep(2)
        self.update_display("hot ___")

    def update_display(self, hint):
        print(f"Updating hint with: {hint}")
        
        potential_words = self.capture_logic.match_words(hint)
        print(f"Updating potential words with: {potential_words}")
        
        self.gui.label_status.config(text=f"Hint: {hint}")
        self.gui.text_display.config(state='normal')
        self.gui.text_display.delete(1.0, tk.END)
        self.gui.text_display.insert(tk.END, potential_words.replace(', ', '\n'))
        self.gui.text_display.config(state='disabled')

        print("Display updated.\n")

    def clear_text_display(self):
        self.gui.text_display.config(state='normal')
        self.gui.text_display.delete(1.0, tk.END)
        self.gui.text_display.config(state='disabled')

    def update_coordinates_display(self):
        self.settings_menu.update_coordinates_display()

    def start_capture(self):
        # Check if the thread is already running
        if not hasattr(self, 'capture_thread') or not self.capture_thread.is_alive():
            print("Starting new capture thread...")

            # Create and start a new thread
            self.capture_thread = threading.Thread(target=self.capture_session, daemon=True)
            self.capture_thread.start()

            print("Capture thread started.\n")
        else:
            print("Capture is already running")

    def capture_session(self):
        print("Capture session started.\n")       

        while self.capturing:
            # Simulate fetching a hint (replace with actual logic)
            hint = self.capture_logic.get_hint()

            # Simulate matching words (replace with actual logic)
            words = self.capture_logic.match_words(hint)

            # Update display with the hint
            self.update_display(hint)

            # Sleep to prevent this loop from consuming too much CPU
            time.sleep(1)

        print("Capture session ended.\n")

    def reload_app(self, event=None):
        print("Reloading...")

        self.save_settings()
        python = sys.executable
        script = f'"{sys.argv[0]}"'
        os.execl(python, python, script)

    def open_settings(self):
        print("Opening settings menu...")
        self.settings_menu.show()
        self.settings_menu.update_coordinates_display()
        print("Settings menu shown.\n")

    def quit_app(self):
        print("Quitting application...")
        self.save_settings()
        sys.exit()
