import customtkinter as ctk
import os
import json

class PresetsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.app = parent
        self.presets_dir = "assets/presets"
        os.makedirs(self.presets_dir, exist_ok=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(self.top_frame, text="Crosshair Presets", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        self.save_button = ctk.CTkButton(self.top_frame, text="Save Current as Preset", command=self.save_preset)
        self.save_button.pack(side="right")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Available Presets")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.create_default_preset_if_needed()
        self.refresh_presets()
    
    def refresh_presets(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            for i, filename in enumerate(os.listdir(self.presets_dir)):
                if filename.endswith(".json"):
                    preset_frame = ctk.CTkFrame(self.scrollable_frame)
                    preset_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
                    preset_frame.grid_columnconfigure(0, weight=1)

                    name_label = ctk.CTkLabel(preset_frame, text=filename.replace(".json", ""), anchor="w")
                    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

                    file_path = os.path.join(self.presets_dir, filename)
                    load_button = ctk.CTkButton(preset_frame, text="Load", width=80,
                                                command=lambda p=file_path: self.load_preset(p))
                    load_button.grid(row=0, column=1, padx=10, pady=10)
        except FileNotFoundError:
            ctk.CTkLabel(self.scrollable_frame, text="Presets directory not found.").pack()

    def load_preset(self, path):
        try:
            with open(path, 'r') as f:
                params = json.load(f)
            
            self.app.views["editor"].load_params(params)
            self.app.switch_view("editor")
        except Exception as e:
            print(f"Failed to load preset: {e}")

    def save_preset(self):
        current_params = self.app.views["editor"].params
        dialog = ctk.CTkInputDialog(text="Enter preset name:", title="Save Preset")
        preset_name = dialog.get_input()

        if preset_name:
            filename = f"{preset_name.strip()}.json"
            file_path = os.path.join(self.presets_dir, filename)
            
            try:
                with open(file_path, 'w') as f:
                    json.dump(current_params, f, indent=4)
                self.refresh_presets()
            except Exception as e:
                print(f"Failed to save preset: {e}")

    def create_default_preset_if_needed(self):
        default_file = os.path.join(self.presets_dir, "default_cross.json")
        if not os.path.exists(default_file):
            default_params = {
                "color": "#00ff00",
                "outline_enabled": True, "outline_thickness": 1.0,
                "center_dot_enabled": False, "center_dot_size": 2.0,
                "inner_lines_enabled": True, "inner_lines_length": 6.0,
                "inner_lines_thickness": 2.0, "inner_lines_offset": 3.0
            }
            with open(default_file, 'w') as f:
                json.dump(default_params, f, indent=4)

    def load_default_preset(self):
        default_file = os.path.join(self.presets_dir, "default_cross.json")
        if os.path.exists(default_file):
            self.load_preset(default_file)
        else:
            self.app.views['editor'].update_crosshair()