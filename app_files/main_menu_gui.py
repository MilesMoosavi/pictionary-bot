import tkinter as tk
from main_menu_logic import MainMenuLogic

class MainMenuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Pictionary Bot')

        self.frame_main = tk.Frame(self.root, padx=10, pady=10)
        self.frame_main.pack(padx=10, pady=10, fill='both', expand=True)

        self.label_status = tk.Label(self.frame_main, text='Capture not in session', font=('Arial', 12))
        self.label_status.pack(pady=(0, 20))

        self.text_display = tk.Text(self.frame_main, height=4, state='disabled')
        self.text_display.pack(fill='both', expand=True)

        self.button_toggle = tk.Button(self.frame_main, text='Start/Stop Capture', command=self.toggle_capture)
        self.button_toggle.pack(fill='x')

        reload_button = tk.Button(self.frame_main, text="Reload App", command=self.reload_app)
        reload_button.pack(side='left', padx=(0, 10))

        self.button_settings = tk.Button(self.frame_main, text='⚙', command=self.open_settings)
        self.button_settings.pack(side='right', padx=(0, 0))

        quit_button = tk.Button(self.frame_main, text="Quit", command=self.quit_app)
        quit_button.pack(side='right', padx=(10, 0))

        self.logic = MainMenuLogic(self)

    def toggle_capture(self):
        self.logic.toggle_capture()

    def reload_app(self):
        self.logic.reload_app()

    def open_settings(self):
        self.logic.open_settings()

    def quit_app(self):
        self.logic.quit_app()

root = tk.Tk()
app = MainMenuGUI(root)
root.focus_force()
root.mainloop()
