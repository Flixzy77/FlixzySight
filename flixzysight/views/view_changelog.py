import customtkinter as ctk

CHANGELOG_TEXT = """
v1.1.2 - Trainer Bug Fix (August 2, 2025)
- Fixed a critical bug where target clicks were not registering correctly.
- Restored the intuitive "click to start" flow.
- Improved gameplay fluidity by reducing delay after a successful hit.

v1.1.1 - Trainer Update & Initial Fix (August 2, 2025)
- Added new "Speed" training mode.
- Added mode selection to the Trainer UI.
- Attempted to fix the hit registration bug.

v1.1 - The Aim Trainer Update (August 2, 2025)
- Added the first version of the Aim Trainer module.
- Implemented "Reaction" mode.
- Added average reaction time tracking.

v1.0 - Early Access (August 2, 2025)
- Parametric editor with live preview implemented.
- JSON-based preset system for saving and loading.
- Global hotkey (F8) to toggle the overlay.

v0.5 - Beta (July 15, 2025)
- Initial pixel-based editor created.
- Basic PNG preset loading.

v0.1 - Pre-Alpha (June 1, 2025)
- Application core and UI structure created.
"""

class ChangelogView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.label = ctk.CTkLabel(self, text="Changelog", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20, padx=20)

        self.textbox = ctk.CTkTextbox(self, width=400, height=300, corner_radius=10)
        self.textbox.insert("0.0", CHANGELOG_TEXT)
        self.textbox.configure(state="disabled")
        self.textbox.pack(pady=10, padx=20, fill="both", expand=True)