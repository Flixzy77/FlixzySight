import customtkinter as ctk
from tkinter import colorchooser

class EditorView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.app = parent
        self.params = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Crosshair Settings")
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.controls = {}
        
        self.create_header(self.scrollable_frame, "General")
        self.controls['color'] = self.create_color_picker(self.scrollable_frame, "Color")
        self.controls['outline_enabled'] = self.create_switch(self.scrollable_frame, "Outlines")
        self.controls['outline_thickness'] = self.create_slider(self.scrollable_frame, "Outline Thickness", 1, 5)

        self.create_header(self.scrollable_frame, "Center Dot")
        self.controls['center_dot_enabled'] = self.create_switch(self.scrollable_frame, "Enabled")
        self.controls['center_dot_size'] = self.create_slider(self.scrollable_frame, "Size", 0, 10)

        self.create_header(self.scrollable_frame, "Inner Lines")
        self.controls['inner_lines_enabled'] = self.create_switch(self.scrollable_frame, "Enabled", default_on=True)
        self.controls['inner_lines_length'] = self.create_slider(self.scrollable_frame, "Length", 1, 20)
        self.controls['inner_lines_thickness'] = self.create_slider(self.scrollable_frame, "Thickness", 1, 10)
        self.controls['inner_lines_offset'] = self.create_slider(self.scrollable_frame, "Offset", 0, 20)
        
        # Initial draw might happen before all controls are ready, so we defer it
        self.after(100, self.update_crosshair)

    def create_header(self, parent, text):
        header = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        header.pack(fill="x", padx=10, pady=(15, 5))
        return header

    def create_slider(self, parent, label_text, from_, to, default_value=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        label.pack(side="left")
        
        slider = ctk.CTkSlider(frame, from_=from_, to=to)
        slider.pack(side="left", fill="x", expand=True, padx=10)
        
        value_label = ctk.CTkLabel(frame, text=f"{slider.get():.0f}", width=30)
        value_label.pack(side="right")
        
        def update_value_label(value):
            value_label.configure(text=f"{float(value):.0f}")
            self.update_crosshair()
            
        slider.configure(command=update_value_label)
        if default_value is not None:
            slider.set(default_value)
            
        return slider

    def create_switch(self, parent, label_text, default_on=False):
        switch_var = ctk.StringVar(value="on" if default_on else "off")
        switch = ctk.CTkSwitch(parent, text=label_text, variable=switch_var, onvalue="on", offvalue="off", command=self.update_crosshair)
        switch.pack(fill="x", padx=10, pady=5)
        return switch

    def create_color_picker(self, parent, label_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        label.pack(side="left")
        
        color_button = ctk.CTkButton(frame, text="", width=50, fg_color="#00FF00", command=self.pick_color)
        color_button.pack(side="left", padx=10)
        return color_button
        
    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code and color_code[1]:
            self.controls['color'].configure(fg_color=color_code[1])
            self.update_crosshair()

    def update_crosshair(self, *_):
        self.params['color'] = self.controls['color'].cget("fg_color")
        self.params['outline_enabled'] = self.controls['outline_enabled'].get() == "on"
        self.params['outline_thickness'] = self.controls['outline_thickness'].get()
        
        self.params['center_dot_enabled'] = self.controls['center_dot_enabled'].get() == "on"
        self.params['center_dot_size'] = self.controls['center_dot_size'].get()
        
        self.params['inner_lines_enabled'] = self.controls['inner_lines_enabled'].get() == "on"
        self.params['inner_lines_length'] = self.controls['inner_lines_length'].get()
        self.params['inner_lines_thickness'] = self.controls['inner_lines_thickness'].get()
        self.params['inner_lines_offset'] = self.controls['inner_lines_offset'].get()
        
        self.app.overlay_window.draw_crosshair_from_params(self.params)
        
        if not self.app.overlay_window.is_visible:
            self.app.overlay_window.show_overlay()
            self.app.views['overlay'].update_switch_state()
            
    def load_params(self, params):
        self.controls['color'].configure(fg_color=params.get("color", "#00FF00"))
        
        if params.get("outline_enabled"): self.controls['outline_enabled'].select() 
        else: self.controls['outline_enabled'].deselect()
        self.controls['outline_thickness'].set(params.get("outline_thickness", 1))
        
        if params.get("center_dot_enabled"): self.controls['center_dot_enabled'].select()
        else: self.controls['center_dot_enabled'].deselect()
        self.controls['center_dot_size'].set(params.get("center_dot_size", 2))
        
        if params.get("inner_lines_enabled", True): self.controls['inner_lines_enabled'].select()
        else: self.controls['inner_lines_enabled'].deselect()
        self.controls['inner_lines_length'].set(params.get("inner_lines_length", 6))
        self.controls['inner_lines_thickness'].set(params.get("inner_lines_thickness", 2))
        self.controls['inner_lines_offset'].set(params.get("inner_lines_offset", 2))
        
        self.update_crosshair()