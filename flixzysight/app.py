import customtkinter as ctk
from .ui_components.sidebar import Sidebar
from .views.view_overlay import OverlayView
from .views.view_editor import EditorView
from .views.view_presets import PresetsView
from .views.view_trainer import TrainerView
from .views.view_settings import SettingsView
from .views.view_changelog import ChangelogView
from .core.crosshair_overlay import CrosshairOverlay
from .core.hotkey_manager import HotkeyManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎯 FlixzySight – Crosshair Overlay & Aim Trainer")
        self.geometry("900x650")
        self.minsize(800, 600)
        ctk.set_appearance_mode("Dark")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.overlay_window = CrosshairOverlay(self)
        
        self.hotkey_manager = HotkeyManager("119", self.toggle_overlay_visibility) # 119 to kod dla F8
        self.hotkey_manager.start()

        self.views = {}
        self.sidebar = Sidebar(self, self.switch_view)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # --- POPRAWIONA KOLEJNOŚĆ INICJALIZACJI ---
        # 1. Stwórz kluczowe widoki, od których zależą inne
        overlay_view = OverlayView(self, self.overlay_window)
        self.views["overlay"] = overlay_view
        
        editor_view = EditorView(self)
        self.views["editor"] = editor_view
        
        # 2. Stwórz pozostałe widoki
        for ViewClass in (PresetsView, TrainerView, SettingsView, ChangelogView):
            name = ViewClass.__name__.replace("View", "").lower()
            view = ViewClass(self) 
            self.views[name] = view

        # 3. Umieść wszystkie widoki w siatce (grid)
        for view in self.views.values():
            view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # 4. Wyświetl domyślny widok
        self.switch_view("editor") # Zmieniamy domyślny widok na edytor
        
        # 5. Załaduj domyślny preset przy starcie
        self.views["presets"].load_default_preset()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_overlay_visibility(self):
        self.overlay_window.toggle_visibility()
        self.views["overlay"].update_switch_state()

    def switch_view(self, view_name):
        view = self.views.get(view_name)
        if view:
            if view_name == 'presets': # Odśwież presety przy każdym przejściu
                view.refresh_presets()
            view.tkraise()

    def on_closing(self):
        self.hotkey_manager.stop()
        self.destroy()