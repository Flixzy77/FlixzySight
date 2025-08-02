import threading
from pynput import keyboard

class HotkeyManager:
    def __init__(self, keycode_str, callback):
        self.hotkey_str = "F8"  # Default display name
        self.callback = callback
        self.hotkey = keyboard.HotKey(keyboard.HotKey.parse(f'<{keycode_str}>'), self.callback)
        
        self.listener = keyboard.Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release)
        )
        self.listener_thread = None

    def for_canonical(self, f):
        return lambda k: f(self.listener.canonical(k))

    def start(self):
        if self.listener_thread is None or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(target=self.listener.run, daemon=True)
            self.listener_thread.start()
            print("Hotkey listener started.")

    def stop(self):
        if self.listener is not None and self.listener.is_alive():
            self.listener.stop()
            # Czekamy na zakończenie wątku, aby uniknąć błędów
            if self.listener_thread is not None:
                 self.listener_thread.join()
            print("Hotkey listener stopped.")

    def update_hotkey(self, new_keycode_str):
        """Stops the current listener and starts a new one with a new hotkey."""
        self.stop()
        
        # Stwórz nowy obiekt HotKey i Listener
        try:
            self.hotkey = keyboard.HotKey(keyboard.HotKey.parse(f'<{new_keycode_str}>'), self.callback)
            self.listener = keyboard.Listener(
                on_press=self.for_canonical(self.hotkey.press),
                on_release=self.for_canonical(self.hotkey.release)
            )
            self.start()
            print(f"Hotkey updated to <{new_keycode_str}>")
            return True
        except Exception as e:
            print(f"Failed to update hotkey: {e}. Reverting to old hotkey.")
            # W razie błędu, spróbuj przywrócić stary listener
            self.start()
            return False