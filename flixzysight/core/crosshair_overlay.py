import customtkinter as ctk
from PIL import Image, ImageDraw

class CrosshairOverlay(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.transparent_color = '#000001'
        self.wm_attributes("-transparentcolor", self.transparent_color)
        self.configure(fg_color=self.transparent_color)
        self.is_visible = False
        self.crosshair_ctk_image = None
        self.label = ctk.CTkLabel(self, text="", fg_color=self.transparent_color)
        self.label.pack(fill="both", expand=True)
        self.withdraw()

    def update_image(self, ctk_image):
        self.crosshair_ctk_image = ctk_image
        self.label.configure(image=self.crosshair_ctk_image)
        self.geometry(f"{ctk_image.cget('size')[0]}x{ctk_image.cget('size')[1]}")
        if self.is_visible:
            self.center_window()

    def _draw_single_crosshair(self, draw_context, params, color, offset=(0, 0)):
        center_x = (params["size"] / 2) + offset[0]
        center_y = (params["size"] / 2) + offset[1]

        if params.get("center_dot_enabled", False):
            s = params.get("center_dot_size", 2.0)
            if s > 0:
                draw_context.rectangle([center_x - s, center_y - s, center_x + s, center_y + s], fill=color)
        
        if params.get("inner_lines_enabled", True):
            l = params.get("inner_lines_length", 6.0)
            t = params.get("inner_lines_thickness", 2.0)
            o = params.get("inner_lines_offset", 2.0)
            ht = t / 2.0
            
            draw_context.rectangle([center_x - ht, center_y - o - l, center_x + ht, center_y - o], fill=color)
            draw_context.rectangle([center_x - ht, center_y + o, center_x + ht, center_y + o + l], fill=color)
            draw_context.rectangle([center_x - o - l, center_y - ht, center_x - o, center_y + ht], fill=color)
            draw_context.rectangle([center_x + o, center_y - ht, center_x + o + l, center_y + ht], fill=color)

    def draw_crosshair_from_params(self, params):
        final_size = 100
        scale = 4
        scaled_size = final_size * scale
        
        scaled_params = params.copy()
        scaled_params["size"] = scaled_size
        for key in ["center_dot_size", "inner_lines_length", "inner_lines_thickness", "inner_lines_offset"]:
            if key in scaled_params:
                scaled_params[key] *= scale

        image = Image.new("RGBA", (scaled_size, scaled_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        main_color = params.get("color", "#9370DB")
        
        if params.get("outline_enabled", False) and params.get("outline_thickness", 0) > 0:
            outline_color = "#000000"
            thickness = params.get("outline_thickness", 1.0) * scale
            loop_range = range(-round(thickness), round(thickness) + 1)

            for x_offset in loop_range:
                for y_offset in loop_range:
                    if x_offset == 0 and y_offset == 0: continue
                    self._draw_single_crosshair(draw, scaled_params, outline_color, offset=(x_offset, y_offset))

        self._draw_single_crosshair(draw, scaled_params, main_color)
        
        # *** TUTAJ KLUCZOWA ZMIANA: ZAWSZE UŻYWAMY FILTRA "NEAREST" ***
        # Ten filtr gwarantuje ostre, pikselowe krawędzie bez żadnego wygładzania.
        resized_image = image.resize((final_size, final_size), Image.Resampling.NEAREST)
        
        background = Image.new("RGB", resized_image.size, self.transparent_color)
        background.paste(resized_image, (0, 0), resized_image)
        
        return ctk.CTkImage(light_image=background, dark_image=background, size=(final_size, final_size))

    def center_window(self):
        self.update_idletasks()
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        width, height = self.winfo_width(), self.winfo_height()
        x, y = (screen_width // 2) - (width // 2), (screen_height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def show_overlay(self):
        self.is_visible = True
        self.deiconify()
        self.lift()
        self.wm_attributes("-topmost", True)
        self.center_window()

    def hide_overlay(self):
        self.is_visible = False
        self.withdraw()

    def toggle_visibility(self):
        if self.is_visible: self.hide_overlay()
        else: self.show_overlay()