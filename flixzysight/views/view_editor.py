import customtkinter as ctk
from tkinter import colorchooser
import os
import json
import base64
import pyperclip
import sys

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ACCENT_COLOR = "#9370DB"
FRAME_COLOR = "#242424"
BG_COLOR = "#1B1B1B"
HOVER_COLOR = "#333333"

class EditorView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR)
        self.app = parent
        self.params = {}
        self.profiles_dir = resource_path("assets/presets")
        self.thumbnail_references = []
        os.makedirs(self.profiles_dir, exist_ok=True)

        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2, minsize=200)
        self.grid_rowconfigure(0, weight=1)

        # --- LEWA KOLUMNA (Profile) ---
        self.profiles_frame = self.create_section_frame(self, "Parametric Profiles")
        self.profiles_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.profiles_scroll_frame = ctk.CTkScrollableFrame(self.profiles_frame, fg_color="transparent")
        self.profiles_scroll_frame.pack(expand=True, fill="both", pady=5, padx=5)
        
        import_export_frame = ctk.CTkFrame(self.profiles_frame, fg_color="transparent")
        import_export_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(import_export_frame, text="Import", fg_color=ACCENT_COLOR, command=self.import_profile).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(import_export_frame, text="Export", fg_color=ACCENT_COLOR, command=self.export_profile).pack(side="left", expand=True, padx=2)

        # --- ŚRODKOWA KOLUMNA (Ustawienia) ---
        self.settings_frame = self.create_section_frame(self, "Crosshair Settings")
        self.settings_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        self.controls_scroll_frame = ctk.CTkScrollableFrame(self.settings_frame, fg_color="transparent")
        self.controls_scroll_frame.pack(expand=True, fill="both", pady=5, padx=5)
        self.controls = {}
        
        self.create_parametric_controls() # Zmieniona nazwa dla jasności
        
        self.save_button = ctk.CTkButton(self.settings_frame, text="Save Current as Profile", command=self.save_profile, fg_color=ACCENT_COLOR)
        self.save_button.pack(fill="x", padx=10, pady=10)

        # --- PRAWA KOLUMNA (Podgląd) ---
        self.preview_frame = self.create_section_frame(self, "Live Preview")
        self.preview_frame.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="nsew")
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="", fg_color=BG_COLOR)
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.after(100, self.load_default_profile)

    def create_parametric_controls(self):
        self.create_header(self.controls_scroll_frame, "General"); self.controls['color'] = self.create_color_picker(self.controls_scroll_frame, "Color", icon_char="🎨"); self.controls['outline_enabled'] = self.create_switch(self.controls_scroll_frame, "Outlines", icon_char="🔳"); self.controls['outline_thickness'] = self.create_slider(self.controls_scroll_frame, "Outline Thickness", 0, 5, icon_char="↔")
        self.create_header(self.controls_scroll_frame, "Center Dot"); self.controls['center_dot_enabled'] = self.create_switch(self.controls_scroll_frame, "Enabled", icon_char="●"); self.controls['center_dot_size'] = self.create_slider(self.controls_scroll_frame, "Size", 0, 10, icon_char="↔")
        self.create_header(self.controls_scroll_frame, "Inner Lines"); self.controls['inner_lines_enabled'] = self.create_switch(self.controls_scroll_frame, "Enabled", default_on=True, icon_char="╋"); self.controls['inner_lines_length'] = self.create_slider(self.controls_scroll_frame, "Length", 1, 20, icon_char="↕"); self.controls['inner_lines_thickness'] = self.create_slider(self.controls_scroll_frame, "Thickness", 1, 10, icon_char="↔"); self.controls['inner_lines_offset'] = self.create_slider(self.controls_scroll_frame, "Offset", 0, 20, icon_char="✥")

    def create_section_frame(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=FRAME_COLOR, corner_radius=8)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x", padx=15, pady=(8, 4))
        return frame

    def create_header(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=13, weight="bold"), anchor="w").pack(fill="x", padx=10, pady=(15, 5))

    def create_slider(self, parent, label_text, from_, to, icon_char=None, is_int=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent"); frame.pack(fill="x", padx=10, pady=5)
        if icon_char: ctk.CTkLabel(frame, text=icon_char, font=ctk.CTkFont(size=18), width=20).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(frame, text=label_text, width=120, anchor="w").pack(side="left")
        slider = ctk.CTkSlider(frame, from_=from_, to=to, button_color=ACCENT_COLOR, progress_color=ACCENT_COLOR); slider.pack(side="left", fill="x", expand=True, padx=10)
        format_str = "{:.0f}" if is_int else "{:.2f}"; value_label = ctk.CTkLabel(frame, text=format_str.format(slider.get()), width=40); value_label.pack(side="right")
        slider.configure(command=lambda v, l=value_label: (l.configure(text=format_str.format(v)), self.update_crosshair())); return slider

    def create_switch(self, parent, label_text, default_on=False, icon_char=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent"); frame.pack(fill="x", padx=10, pady=5, anchor="w")
        if icon_char: ctk.CTkLabel(frame, text=icon_char, font=ctk.CTkFont(size=18), width=20).pack(side="left", padx=(0, 8))
        switch = ctk.CTkSwitch(frame, text=label_text, command=self.update_crosshair, progress_color=ACCENT_COLOR)
        if default_on: switch.select()
        switch.pack(side="left"); return switch

    def create_color_picker(self, parent, label_text, icon_char=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent"); frame.pack(fill="x", padx=10, pady=5)
        if icon_char: ctk.CTkLabel(frame, text=icon_char, font=ctk.CTkFont(size=18), width=20).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(frame, text=label_text, width=120, anchor="w").pack(side="left")
        color_button = ctk.CTkButton(frame, text="", width=32, height=32, fg_color=ACCENT_COLOR, command=self.pick_color, hover_color=ACCENT_COLOR); color_button.pack(side="left", padx=10)
        return color_button
        
    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code and color_code[1]: self.controls['color'].configure(fg_color=color_code[1]); self.update_crosshair()

    def update_crosshair(self, *_):
        for key, control in self.controls.items():
            if isinstance(control, ctk.CTkSlider): self.params[key] = control.get()
            elif isinstance(control, ctk.CTkSwitch): self.params[key] = control.get() == 1
            elif isinstance(control, ctk.CTkButton): self.params[key] = control.cget("fg_color")
        new_image = self.app.overlay_window.draw_crosshair_from_params(self.params)
        self.app.overlay_window.update_image(new_image)
        self.preview_label.configure(image=new_image)
        if not self.app.overlay_window.is_visible: self.app.overlay_window.show_overlay(); self.app.views['overlay'].update_switch_state()

    def load_params(self, params):
        self.controls['color'].configure(fg_color=params.get("color", ACCENT_COLOR))
        self.controls['outline_enabled'].select() if params.get("outline_enabled") else self.controls['outline_enabled'].deselect()
        for key in ["outline_thickness", "center_dot_size", "inner_lines_length", "inner_lines_thickness", "inner_lines_offset"]:
            if key in self.controls: self.controls[key].set(params.get(key, 1))
        self.controls['center_dot_enabled'].select() if params.get("center_dot_enabled") else self.controls['center_dot_enabled'].deselect()
        self.controls['inner_lines_enabled'].select() if params.get("inner_lines_enabled", True) else self.controls['inner_lines_enabled'].deselect()
        self.update_crosshair()

    def refresh_profiles(self):
        for widget in self.profiles_scroll_frame.winfo_children(): widget.destroy()
        self.thumbnail_references.clear()
        try:
            for filename in sorted(os.listdir(self.profiles_dir)):
                if filename.endswith(".json"): # Ten edytor obsługuje tylko JSON
                    path = os.path.join(self.profiles_dir, filename)
                    name = os.path.splitext(filename)[0]
                    profile_entry = ctk.CTkFrame(self.profiles_scroll_frame, fg_color="transparent", corner_radius=6); profile_entry.pack(fill="x", padx=5, pady=3)
                    with open(path, 'r') as f: params = json.load(f)
                    thumb_image = self.app.overlay_window.draw_crosshair_from_params(params); self.thumbnail_references.append(thumb_image)
                    thumbnail_label = ctk.CTkLabel(profile_entry, image=thumb_image, text="", width=40, height=40, fg_color=BG_COLOR); thumbnail_label.pack(side="left", padx=5, pady=5)
                    name_label = ctk.CTkLabel(profile_entry, text=name, anchor="w"); name_label.pack(side="left", expand=True, fill="x", padx=10)
                    for widget in (profile_entry, name_label, thumbnail_label):
                        widget.bind("<Enter>", lambda e, w=profile_entry: w.configure(fg_color=HOVER_COLOR)); widget.bind("<Leave>", lambda e, w=profile_entry: w.configure(fg_color="transparent")); widget.bind("<Button-1>", lambda e, p=path: self.load_profile(p))
        except Exception as e: print(f"Refresh profiles error: {e}")
    
    def load_profile(self, path):
        try:
            with open(path, 'r') as f: self.load_params(json.load(f))
        except Exception as e: print(f"Failed to load profile: {e}")

    def load_default_profile(self):
        default_file = os.path.join(self.profiles_dir, "default_cross.json")
        if not os.path.exists(default_file):
            params = {"color":ACCENT_COLOR,"outline_enabled":True,"outline_thickness":1.0,"center_dot_enabled":False,"center_dot_size":2.0,"inner_lines_enabled":True,"inner_lines_length":6.0,"inner_lines_thickness":2.0,"inner_lines_offset":3.0}
            with open(default_file, 'w') as f: json.dump(params, f, indent=4)
        self.load_profile(default_file); self.refresh_profiles()

    def save_profile(self):
        dialog = ctk.CTkInputDialog(text="Enter profile name:", title="Save Parametric Profile")
        name = dialog.get_input()
        if name:
            path = os.path.join(self.profiles_dir, f"{name.strip()}.json")
            with open(path, 'w') as f: json.dump(self.params, f, indent=4)
            print(f"Profile saved: {path}"); self.refresh_profiles()

    def export_profile(self):
        try:
            json_string=json.dumps(self.params); encoded=base64.b64encode(json_string.encode('utf-8')).decode('utf-8'); pyperclip.copy(encoded); print("✅ Parametric profile code copied.")
        except Exception as e: print(f"❌ Export failed: {e}")

    def import_profile(self):
        dialog = ctk.CTkInputDialog(text="Paste your profile code here:", title="Import Profile")
        code = dialog.get_input()
        if code:
            try:
                decoded=base64.b64decode(code).decode('utf-8'); params=json.loads(decoded); self.load_params(params); print("✅ Profile imported successfully.")
            except Exception as e: print(f"❌ Import failed. Invalid code: {e}")