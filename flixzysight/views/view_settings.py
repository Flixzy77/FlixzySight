import customtkinter as ctk

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, hotkey_manager):
        super().__init__(parent, fg_color="transparent")
        self.app = parent
        self.hotkey_manager = hotkey_manager
        
        self.is_listening = False

        # --- Tytuł ---
        ctk.CTkLabel(self, text="Application Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=10, pady=(0, 20))

        # --- Sekcja wyglądu ---
        appearance_frame = ctk.CTkFrame(self, border_width=1, border_color="#333")
        appearance_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(appearance_frame, text="Appearance", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        
        theme_selector = ctk.CTkSegmentedButton(
            appearance_frame,
            values=["Light", "Dark", "System"],
            command=self.change_theme
        )
        theme_selector.set("Dark")
        theme_selector.pack(fill="x", padx=15, pady=(5, 15))

        # --- Sekcja Hotkey ---
        hotkey_frame = ctk.CTkFrame(self, border_width=1, border_color="#333")
        hotkey_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(hotkey_frame, text="Overlay Hotkey", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,5))

        self.hotkey_button = ctk.CTkButton(hotkey_frame, text=f"Current: {self.hotkey_manager.hotkey_str}", command=self.start_listening)
        self.hotkey_button.pack(fill="x", padx=15, pady=(5, 15))
        
        self.info_label = ctk.CTkLabel(hotkey_frame, text="Click to change. Press Esc to cancel.", text_color="gray")
        self.info_label.pack(pady=(0,10))


    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme.lower())

    def start_listening(self):
        if self.is_listening: return
        self.is_listening = True
        self.hotkey_button.configure(text="Press any key...")
        self.app.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        if not self.is_listening: return
        
        # Zakończ nasłuchiwanie w GUI
        self.app.unbind("<KeyPress>")
        self.is_listening = False
        
        # Anulowanie przez Escape
        if event.keysym == 'Escape':
            self.hotkey_button.configure(text=f"Current: {self.hotkey_manager.hotkey_str}")
            return
            
        # Spróbuj przetworzyć klawisz
        new_key_display = event.keysym.upper()
        new_keycode = event.keycode
        
        # pynput używa kodów, a nie keysym dla klawiszy funkcyjnych F1-F12
        if "F" in new_key_display and len(new_key_display) > 1 and new_key_display[1:].isdigit():
            f_number = int(new_key_display[1:])
            # Kody dla F1-F12 zaczynają się od 112
            new_keycode_str = str(111 + f_number)
        else:
            new_keycode_str = str(new_keycode)

        # Zaktualizuj menedżera i przycisk
        if self.hotkey_manager.update_hotkey(new_keycode_str):
            self.hotkey_manager.hotkey_str = new_key_display
            self.hotkey_button.configure(text=f"Current: {new_key_display}")
        else:
            # Jeśli aktualizacja się nie powiedzie, przywróć stary tekst
            self.hotkey_button.configure(text=f"Current: {self.hotkey_manager.hotkey_str}")