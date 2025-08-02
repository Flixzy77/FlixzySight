import customtkinter as ctk

CHANGELOG_TEXT = """
v2.0.0 - The Phoenix Update (August 2, 2025)

### Major Features & UI Overhaul
- Complete GUI redesign for a modern, professional look and feel.
- Implemented a new three-column editor layout, integrating Profiles, Settings, and a Live Preview into a single, efficient workspace.
- Introduced a new, consistent purple-accented dark theme.
- The sidebar has been modernized with a clear visual indicator for the active view.
- Added an in-app Live Preview window for instant visual feedback.
- Added profile thumbnail previews, allowing users to see saved crosshairs at a glance.
- Implemented profile Import/Export via a text code for easy sharing.

### Editor & Rendering Enhancements
- Editor sliders now support floating-point values for high-precision adjustments.
- Implemented a new supersampling rendering engine for a crisp, pixel-perfect crosshair aesthetic (anti-aliasing has been removed).
- Rewrote the crosshair outline algorithm for a clean, pixel-perfect contour.
- Added descriptive Unicode icons next to each setting for improved clarity.
- Added new profiles:  [+]Blue Pill [+]Lemon Haze

### Bug Fixes
- Fixed a critical bug causing the overlay to render with a solid black background instead of being transparent.
- Fixed all known bugs related to the Light Theme, ensuring all UI elements display correctly.

v1.2.2 - Light Theme Text Fix (August 2, 2025)
- Fixed a bug where sidebar button text was not visible in the light theme.

v1.2.1 - Theme Fix (August 2, 2025)
- Fixed a bug where the sidebar and title text did not update correctly when switching to the light theme.
- Improved hover colors for sidebar buttons in both themes.

v1.2 - The Polish & Settings Update (August 2, 2025)
- Implemented the 'Settings' tab with theme and hotkey customization.
- Complete UI overhaul for a more modern and consistent look.
- Added custom styling for sliders, buttons, and frames.
- Improved layout and spacing across all views.

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