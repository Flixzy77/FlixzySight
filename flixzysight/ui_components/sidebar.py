import customtkinter as ctk

ACCENT_COLOR = "#9370DB"
BG_COLOR = "#1B1B1B"
FRAME_COLOR = "#242424"

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, view_switcher):
        super().__init__(parent, corner_radius=0, fg_color=FRAME_COLOR)
        self.grid_rowconfigure(6, weight=1) # Zmniejszamy row, bo jest mniej przycisków
        self.view_switcher = view_switcher
        self.buttons = {}

        self.logo_label = ctk.CTkLabel(self, text="FlixzySight", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        buttons_info = [
            ("editor", "🎨 Parametric Editor"),
            ("trainer", "🧠 Aim Trainer"),
            ("overlay", "🎯 Overlay"),
            ("settings", "⚙️ Settings"),
        ]
        
        for i, (name, text) in enumerate(buttons_info):
            button = ctk.CTkButton(
                self, text=text, command=lambda n=name: self.button_click(n),
                anchor="w", corner_radius=8, fg_color="transparent",
                hover_color=BG_COLOR, text_color=("#1A1A1A", "#DCE4EE")
            )
            button.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
            self.buttons[name] = button

        changelog_button = ctk.CTkButton(
            self, text="🕘 Changelog", command=lambda: self.button_click("changelog"),
            anchor="w", corner_radius=8, fg_color="transparent",
            hover_color=BG_COLOR, text_color=("gray50", "gray50")
        )
        changelog_button.grid(row=7, column=0, padx=10, pady=10, sticky="s")
        self.buttons["changelog"] = changelog_button

    def button_click(self, view_name):
        self.view_switcher(view_name)
        self.highlight_button(view_name)

    def highlight_button(self, active_button_name):
        for name, button in self.buttons.items():
            if name == active_button_name:
                button.configure(fg_color=ACCENT_COLOR)
            else:
                button.configure(fg_color="transparent")