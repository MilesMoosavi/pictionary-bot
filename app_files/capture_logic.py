import pytesseract
from PIL import ImageGrab
import time

class CaptureLogic:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.running = False
        self.area = (0, 0, 300, 300)  # Default capture area

    def set_area(self, x1, y1, x2, y2):
        self.area = (x1, y1, x2, y2)

    def start_capture(self):
        self.running = True
        self.capture_loop()

    def stop_capture(self):
        self.running = False

    def capture_loop(self):
        previous_text = ""
        while self.running:
            img = ImageGrab.grab(bbox=self.area)
            text = pytesseract.image_to_string(img)
            if text != previous_text:
                previous_text = text
                self.update_callback(text)
            time.sleep(1)  # Reduce frequency to decrease CPU usage

    def get_hint(self):
        # Simulate getting a hint from the captured area
        return "hot ___"

    def match_words(self, hint):
        # Simulate word matching logic for the placeholder hint
        if "hot" in hint:
            return "hot dog, hot pot, top hat"
        return ""

    def update_word_list(self, text):
        hint = self.get_hint()
        self.update_callback(hint)