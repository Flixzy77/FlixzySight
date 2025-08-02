import customtkinter as ctk
from .ui_components.sidebar import Sidebar
from .views.view_overlay import OverlayView
from .views.view_editor import EditorView
# Usunięty import PixelEditorView
from .views.view_trainer import TrainerView
from .views.view_settings import SettingsView
from .views.view_changelog import ChangelogView
from .core.crosshair_overlay import CrosshairOverlay
from .core.hotkey_manager import HotkeyManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎯 FlixzySight v2.1")
        self.geometry("1000x700")
        self.minsize(900, 600)
        ctk.set_appearance_mode("Dark")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.overlay_window = CrosshairOverlay(self)
        self.hotkey_manager = HotkeyManager("119", self.toggle_overlay_visibility)
        self.hotkey_manager.start()

        self.views = {}
        self.sidebar = Sidebar(self, self.switch_view)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        self.create_views()
        
        self.switch_view("editor", initial_load=True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_views(self):
        """Tworzy i umieszcza wszystkie widoki w oknie we właściwej kolejności."""
        
        self.views["overlay"] = OverlayView(self, self.overlay_window)
        self.views["settings"] = SettingsView(self, self.hotkey_manager)

        # Usunęliśmy PixelEditorView z tej listy
        remaining_views = (EditorView, TrainerView, ChangelogView)
        for ViewClass in remaining_views:
            name = ViewClass.__name__.replace("View", "").lower()
            self.views[name] = ViewClass(self)

        for view in self.views.values():
            view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            view.grid_remove()

    def toggle_overlay_visibility(self):
        self.overlay_window.toggle_visibility()
        if "overlay" in self.views:
            self.views["overlay"].update_switch_state()

    def switch_view(self, view_name, initial_load=False):
        """Przełącza widok i aktualizuje podświetlenie w sidebarze."""
        
        for view in self.views.values():
            view.grid_remove()

        view_to_show = self.views.get(view_name)
        if view_to_show:
            view_to_show.grid()
            
            if view_name == 'editor' and initial_load:
                self.after(100, view_to_show.load_default_profile)
            
            if hasattr(view_to_show, 'refresh_profiles'):
                view_to_show.refresh_profiles()
            
            self.sidebar.highlight_button(view_name)

    def on_closing(self):
        self.hotkey_manager.stop()
        self.destroy()