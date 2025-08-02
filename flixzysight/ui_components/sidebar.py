import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, view_switcher):
        # Zmieniamy stały kolor na dynamiczny, zależny od motywu
        # Format: (kolor_dla_light_mode, kolor_dla_dark_mode)
        super().__init__(parent, corner_radius=0, fg_color=("#E5E5E5", "#212121"))
        self.grid_rowconfigure(7, weight=1)

        self.logo_label = ctk.CTkLabel(self, text="FlixzySight", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        buttons_info = [
            ("editor", "🎨 Editor"),
            ("presets", "📁 Presets"),
            ("trainer", "🧠 Aim Trainer"),
            ("overlay", "🎯 Overlay"),
            ("settings", "⚙️ Settings"),
            ("changelog", "🕘 Changelog")
        ]

        self.buttons = {}
        for i, (name, text) in enumerate(buttons_info):
            button = ctk.CTkButton(
                self,
                text=text,
                command=lambda n=name: view_switcher(n),
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                # Kolor po najechaniu również musi być dynamiczny
                hover_color=("#D5D5D5", "#2b2b2b"),
                text_color_disabled="gray"
            )
            button.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
            self.buttons[name] = button