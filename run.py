import os
import sys

# Ensure the app_files directory is in the system path for imports
app_files_path = os.path.join(os.path.dirname(__file__), 'app_files')
sys.path.append(app_files_path)

from main_menu_gui import *
