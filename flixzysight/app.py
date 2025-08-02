import customtkinter as ctk
from .ui_components.sidebar import Sidebar
from .views.view_overlay import OverlayView
from .views.view_editor import EditorView
from .views.view_trainer import TrainerView
from .views.view_settings import SettingsView
from .views.view_changelog import ChangelogView
from .core.crosshair_overlay import CrosshairOverlay
from .core.hotkey_manager import HotkeyManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎯 FlixzySight v2.0")
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

        # Inicjalizacja widoków
        for ViewClass in (EditorView, TrainerView, OverlayView, SettingsView, ChangelogView):
            name = ViewClass.__name__.replace("View", "").lower()
            if name == "settings":
                view = ViewClass(self, self.hotkey_manager)
            elif name == "overlay":
                view = ViewClass(self, self.overlay_window)
            else:
                view = ViewClass(self)
            self.views[name] = view
            view.grid(row=0, column=1, sticky="nsew")
        
        # Ustawienie początkowego widoku i podświetlenia
        self.switch_view("editor", initial_load=True)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_overlay_visibility(self):
        self.overlay_window.toggle_visibility()
        if "overlay" in self.views: self.views["overlay"].update_switch_state()

    def switch_view(self, view_name, initial_load=False):
        """Przełącza widok i aktualizuje podświetlenie w sidebarze."""
        view = self.views.get(view_name)
        if view:
            # Odśwież listę profili przy przejściu do edytora
            if view_name == 'editor':
                # Przy pierwszym ładowaniu aplikacja musi załadować domyślny profil
                if initial_load:
                    self.after(100, view.load_default_profile)
                else:
                    view.refresh_profiles()
            
            view.tkraise()
            # Poinformuj sidebar, który przycisk ma być podświetlony
            self.sidebar.highlight_button(view_name)

    def on_closing(self):
        self.hotkey_manager.stop()
        self.destroy()