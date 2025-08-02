import customtkinter as ctk
import random
import time

class TrainerView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.app = parent

        # --- Stan gry ---
        self.game_running = False
        self.target_visible = False
        self.start_time = 0
        self.reaction_times = []

        # --- Konfiguracja layoutu ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Panel boczny ze statystykami i kontrolkami (lewa strona) ---
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ns")
        
        ctk.CTkLabel(self.controls_frame, text="Aim Trainer", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20, padx=20)

        self.start_button = ctk.CTkButton(self.controls_frame, text="Start Training", command=self.start_game)
        self.start_button.pack(pady=10, padx=20, fill="x")

        self.stop_button = ctk.CTkButton(self.controls_frame, text="Stop Training", command=self.stop_game, state="disabled")
        self.stop_button.pack(pady=5, padx=20, fill="x")
        
        # Statystyki
        ctk.CTkLabel(self.controls_frame, text="Statistics", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5), padx=20)
        
        self.avg_reaction_label = ctk.CTkLabel(self.controls_frame, text="Avg. Reaction: -- ms")
        self.avg_reaction_label.pack(pady=5, padx=20, anchor="w")
        
        self.last_reaction_label = ctk.CTkLabel(self.controls_frame, text="Last Reaction: -- ms")
        self.last_reaction_label.pack(pady=5, padx=20, anchor="w")

        self.hits_label = ctk.CTkLabel(self.controls_frame, text="Hits: 0")
        self.hits_label.pack(pady=5, padx=20, anchor="w")


        # --- Płótno gry (prawa strona) ---
        self.game_canvas = ctk.CTkCanvas(self, bg="#1c1c1c", highlightthickness=0)
        self.game_canvas.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.game_canvas.bind("<Button-1>", self.on_canvas_click)

    def start_game(self):
        if self.game_running:
            return
        
        self.game_running = True
        self.reaction_times = []
        self.update_stats()

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Usuń ewentualne stare cele
        self.game_canvas.delete("target")
        self.game_canvas.delete("message")

        # Wyświetl komunikat startowy
        self.game_canvas.create_text(
            self.game_canvas.winfo_width() / 2,
            self.game_canvas.winfo_height() / 2,
            text="Click to start...",
            fill="white",
            font=("Arial", 20),
            tags="message"
        )

    def stop_game(self):
        if not self.game_running:
            return
        
        self.game_running = False
        self.target_visible = False
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

        self.game_canvas.delete("target")
        self.game_canvas.delete("message")

    def on_canvas_click(self, event):
        if not self.game_running:
            return

        # Pierwsze kliknięcie rozpoczyna grę
        if not self.reaction_times and not self.target_visible:
            self.game_canvas.delete("message")
            self.spawn_target()
            return

        # Sprawdź, czy kliknięto w cel
        clicked_items = self.game_canvas.find_withtag("target")
        if clicked_items:
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            self.update_stats(reaction_time)
            
            self.game_canvas.delete("target")
            self.target_visible = False
            
            # Pojawienie się nowego celu po krótkiej chwili
            self.after(random.randint(300, 1000), self.spawn_target)

    def spawn_target(self):
        if not self.game_running:
            return
            
        self.game_canvas.delete("target")

        canvas_width = self.game_canvas.winfo_width()
        canvas_height = self.game_canvas.winfo_height()
        
        # Upewnij się, że mamy wymiary płótna
        if canvas_width < 50 or canvas_height < 50:
            self.after(100, self.spawn_target) # Spróbuj ponownie za chwilę
            return

        target_radius = 20
        # Losowa pozycja, z buforem od krawędzi
        x = random.randint(target_radius, canvas_width - target_radius)
        y = random.randint(target_radius, canvas_height - target_radius)

        self.game_canvas.create_oval(
            x - target_radius, y - target_radius,
            x + target_radius, y + target_radius,
            fill="#ff4757", outline="", tags="target"
        )
        
        self.target_visible = True
        self.start_time = time.time()

    def update_stats(self, last_reaction=None):
        hits = len(self.reaction_times)
        self.hits_label.configure(text=f"Hits: {hits}")

        if last_reaction is not None:
            self.last_reaction_label.configure(text=f"Last Reaction: {last_reaction * 1000:.0f} ms")
        else:
            self.last_reaction_label.configure(text="Last Reaction: -- ms")

        if hits > 0:
            avg_time = sum(self.reaction_times) / hits
            self.avg_reaction_label.configure(text=f"Avg. Reaction: {avg_time * 1000:.0f} ms")
        else:
            self.avg_reaction_label.configure(text="Avg. Reaction: -- ms")