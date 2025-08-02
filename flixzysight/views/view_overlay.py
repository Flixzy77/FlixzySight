import customtkinter as ctk

class OverlayView(ctk.CTkFrame):
    def __init__(self, parent, overlay_window):
        super().__init__(parent, fg_color="transparent")
        
        self.overlay_window = overlay_window

        self.label = ctk.CTkLabel(self, text="Overlay Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20, padx=20)

        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            self, 
            text="Enable Crosshair Overlay (Hotkey: F8)", 
            variable=self.switch_var, 
            onvalue="on", 
            offvalue="off",
            command=self.toggle_switch
        )
        self.switch.pack(pady=10, padx=20)

    def toggle_switch(self):
        state = self.switch_var.get()
        if state == "on":
            self.overlay_window.show_overlay()
        else:
            self.overlay_window.hide_overlay()

    def update_switch_state(self):
        if self.overlay_window.is_visible:
            self.switch_var.set("on")
        else:
            self.switch_var.set("off")