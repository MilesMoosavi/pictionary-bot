import os
import sys

# Ensure the app_files directory is in the system path for imports
app_files_path = os.path.join(os.path.dirname(__file__), 'app_files')
sys.path.append(app_files_path)

<<<<<<< Updated upstream
from main_menu_gui import MainMenuGUI

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = MainMenuGUI(root)
    root.focus_force()
    root.mainloop()
=======
from main_menu_gui import *
>>>>>>> Stashed changes
