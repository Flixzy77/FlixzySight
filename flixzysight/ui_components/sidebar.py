import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, view_switcher):
        super().__init__(parent, corner_radius=0)
        self.grid_rowconfigure(7, weight=1)

        self.logo_label = ctk.CTkLabel(self, text="FlixzySight", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        buttons_info = [
            ("editor", "🎨 Edytor"),
            ("presets", "📁 Presety"),
            ("trainer", "🧠 Trening"),
            ("overlay", "🎯 Nakładka"),
            ("settings", "⚙️ Ustawienia"),
            ("changelog", "🕘 Zmiany")
        ]

        self.buttons = {}
        for i, (name, text) in enumerate(buttons_info):
            button = ctk.CTkButton(
                self,
                text=text,
                command=lambda n=name: view_switcher(n),
                anchor="w"
            )
            button.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
            self.buttons[name] = button