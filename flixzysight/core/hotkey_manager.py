import threading
from pynput import keyboard

class HotkeyManager:
    def __init__(self, hotkey_str, callback):
        self.hotkey = keyboard.HotKey(keyboard.HotKey.parse(f'<{hotkey_str}>'), callback)
        self.listener = keyboard.Listener(on_press=self.for_canonical(self.hotkey.press), on_release=self.for_canonical(self.hotkey.release))
        self.listener_thread = None

    def for_canonical(self, f):
        return lambda k: f(self.listener.canonical(k))

    def start(self):
        if self.listener_thread is None or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(target=self.listener.run, daemon=True)
            self.listener_thread.start()
            print("Hotkey listener started.")

    def stop(self):
        if self.listener is not None:
            self.listener.stop()
            print("Hotkey listener stopped.")