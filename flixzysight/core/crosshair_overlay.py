import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

class CrosshairOverlay(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.transparent_color = '#000001'
        self.wm_attributes("-transparentcolor", self.transparent_color)
        
        self.configure(bg=self.transparent_color)

        self.is_visible = False
        self.crosshair_photo = None
        
        self.label = ctk.CTkLabel(self, text="", bg_color=self.transparent_color)
        self.label.pack(fill="both", expand=True)
        
        self.withdraw()

    def update_image(self, pil_image):
        """Updates the overlay window with a new PIL image."""
        try:
            self.crosshair_photo = ImageTk.PhotoImage(pil_image)
            self.label.configure(image=self.crosshair_photo)
            self.geometry(f"{pil_image.width}x{pil_image.height}")
            if self.is_visible:
                self.center_window()
        except Exception as e:
            print(f"Error updating overlay image: {e}")

    def draw_crosshair_from_params(self, params):
        """Draws the crosshair based on a dictionary of parameters."""
        size = 100
        center = size // 2
        
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        color = params.get("color", "#00FF00")
        
        if params.get("outline_enabled", False):
            outline_thickness = int(params.get("outline_thickness", 1))
            outline_color = "#000000"
            
            if params.get("center_dot_enabled", False):
                dot_size = int(params.get("center_dot_size", 2))
                s = dot_size + outline_thickness
                draw.rectangle([center-s, center-s, center+s, center+s], fill=outline_color)
            
            if params.get("inner_lines_enabled", True):
                l = int(params.get("inner_lines_length", 6))
                t = int(params.get("inner_lines_thickness", 2))
                o = int(params.get("inner_lines_offset", 2))
                ot = t + outline_thickness * 2
                
                draw.rectangle([center-ot//2, center-o-l, center+ot//2, center-o], fill=outline_color)
                draw.rectangle([center-ot//2, center+o, center+ot//2, center+o+l], fill=outline_color)
                draw.rectangle([center-o-l, center-ot//2, center-o, center+ot//2], fill=outline_color)
                draw.rectangle([center+o, center-ot//2, center+o+l, center+ot//2], fill=outline_color)

        if params.get("center_dot_enabled", False):
            dot_size = int(params.get("center_dot_size", 2))
            draw.rectangle([center-dot_size, center-dot_size, center+dot_size, center+dot_size], fill=color)
        
        if params.get("inner_lines_enabled", True):
            l = int(params.get("inner_lines_length", 6))
            t = int(params.get("inner_lines_thickness", 2))
            o = int(params.get("inner_lines_offset", 2))
            
            draw.rectangle([center-t//2, center-o-l, center+t//2, center-o], fill=color)
            draw.rectangle([center-t//2, center+o, center+t//2, center+o+l], fill=color)
            draw.rectangle([center-o-l, center-t//2, center-o, center+t//2], fill=color)
            draw.rectangle([center+o, center-t//2, center+o+l, center+t//2], fill=color)

        self.update_image(image)


    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def show_overlay(self):
        self.is_visible = True
        self.center_window()
        self.deiconify()
        self.lift()
        self.wm_attributes("-topmost", True)

    def hide_overlay(self):
        self.is_visible = False
        self.withdraw()

    def toggle_visibility(self):
        if self.is_visible:
            self.hide_overlay()
        else:
            self.show_overlay()