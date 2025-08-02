import customtkinter as ctk

class TrainerView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.label = ctk.CTkLabel(self, text="Aim Trainer (Coming Soon)", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20, padx=20, expand=True)