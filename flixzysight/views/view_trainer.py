import customtkinter as ctk
import random
import time

class TrainerView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.app = parent

        # --- Stan gry ---
        self.game_running = False
        self.first_click_done = False
        self.start_time = 0
        self.reaction_times = []
        self.hits = 0
        self.game_mode = "Reaction"
        self.game_timer_id = None
        self.time_limit = 30

        # --- Konfiguracja layoutu ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Panel boczny (lewa strona) ---
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ns")
        
        ctk.CTkLabel(self.controls_frame, text="Aim Trainer", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20, padx=20)

        ctk.CTkLabel(self.controls_frame, text="Game Mode").pack(pady=(10, 5), padx=20)
        self.mode_selector = ctk.CTkSegmentedButton(self.controls_frame, values=["Reaction", "Speed"], command=self.select_mode)
        self.mode_selector.set("Reaction")
        self.mode_selector.pack(pady=5, padx=20, fill="x")

        self.start_button = ctk.CTkButton(self.controls_frame, text="Start Training", command=self.start_game)
        self.start_button.pack(pady=20, padx=20, fill="x")

        self.stop_button = ctk.CTkButton(self.controls_frame, text="Stop Training", command=self.stop_game, state="disabled")
        self.stop_button.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.controls_frame, text="Statistics", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5), padx=20)
        self.timer_label = ctk.CTkLabel(self.controls_frame, text=f"Time Left: {self.time_limit}.0s")
        self.avg_reaction_label = ctk.CTkLabel(self.controls_frame, text="Avg. Reaction: -- ms")
        self.last_reaction_label = ctk.CTkLabel(self.controls_frame, text="Last Reaction: -- ms")
        self.hits_label = ctk.CTkLabel(self.controls_frame, text="Hits: 0")
        
        # --- Płótno gry (prawa strona) ---
        self.game_canvas = ctk.CTkCanvas(self, bg="#1c1c1c", highlightthickness=0)
        self.game_canvas.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.game_canvas.bind("<Button-1>", self.on_canvas_click)
        self.update_ui_for_mode()

    def select_mode(self, mode):
        self.game_mode = mode
        self.update_ui_for_mode()

    def update_ui_for_mode(self):
        if self.game_mode == "Reaction":
            self.timer_label.pack_forget()
            self.avg_reaction_label.pack(pady=5, padx=20, anchor="w")
            self.last_reaction_label.pack(pady=5, padx=20, anchor="w")
            self.hits_label.pack(pady=5, padx=20, anchor="w")
        elif self.game_mode == "Speed":
            self.avg_reaction_label.pack_forget()
            self.last_reaction_label.pack_forget()
            self.timer_label.pack(pady=5, padx=20, anchor="w")
            self.hits_label.pack(pady=5, padx=20, anchor="w")

    def start_game(self):
        if self.game_running: return
        self.game_running = True
        self.first_click_done = False
        self.reset_stats()
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.mode_selector.configure(state="disabled")

        self.game_canvas.delete("all")
        self.game_canvas.create_text(
            self.winfo_width() / 2.5, self.winfo_height() / 2,
            text="Click anywhere to start...", fill="white", font=("Arial", 20), tags="message"
        )

    def stop_game(self):
        if not self.game_running: return
        self.game_running = False
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.mode_selector.configure(state="normal")

        if self.game_timer_id:
            self.after_cancel(self.game_timer_id)
            self.game_timer_id = None

        self.game_canvas.delete("all")
        self.game_canvas.create_text(
            self.winfo_width() / 2.5, self.winfo_height() / 2,
            text="Game Over!", fill="white", font=("Arial", 20), tags="message"
        )

    def on_canvas_click(self, event):
        if not self.game_running: return

        # Pierwsze kliknięcie rozpoczyna grę
        if not self.first_click_done:
            self.first_click_done = True
            self.game_canvas.delete("message")
            if self.game_mode == "Speed":
                self.countdown(self.time_limit)
            self.spawn_target()
            return

        # *** NOWA, POPRAWNA METODA SPRAWDZANIA KLIKNIĘCIA ***
        # Sprawdź, jaki element jest pod kursorem
        item_id = self.game_canvas.find_withtag("current")
        if not item_id: return # Kliknięto w puste pole

        # Sprawdź, czy kliknięty element ma tag "target"
        item_tags = self.game_canvas.gettags(item_id[0])
        if "target" not in item_tags:
            return # Kliknięto w coś innego

        # Jeśli dotarliśmy tutaj, cel został trafiony
        self.hits += 1
        
        if self.game_mode == "Reaction":
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            self.update_stats(last_reaction=reaction_time)
        else: # Speed mode
            self.update_stats()

        self.game_canvas.delete("target")
        self.after(random.randint(50, 250), self.spawn_target)

    def spawn_target(self):
        if not self.game_running: return
            
        canvas_width = self.game_canvas.winfo_width()
        canvas_height = self.game_canvas.winfo_height()
        if canvas_width < 50 or canvas_height < 50:
            self.after(100, self.spawn_target); return

        target_radius = 20
        x = random.randint(target_radius, canvas_width - target_radius)
        y = random.randint(target_radius, canvas_height - target_radius)

        self.game_canvas.create_oval(
            x - target_radius, y - target_radius,
            x + target_radius, y + target_radius,
            fill="#ff4757", outline="", tags="target"
        )
        self.start_time = time.time()

    def countdown(self, remaining_time):
        self.timer_label.configure(text=f"Time Left: {remaining_time:.1f}s")
        if remaining_time > 0 and self.game_running:
            self.game_timer_id = self.after(100, self.countdown, remaining_time - 0.1)
        elif self.game_running:
            self.stop_game()

    def reset_stats(self):
        self.reaction_times = []
        self.hits = 0
        self.update_stats()
        if self.game_mode == "Speed":
            self.timer_label.configure(text=f"Time Left: {self.time_limit}.0s")

    def update_stats(self, last_reaction=None):
        self.hits_label.configure(text=f"Hits: {self.hits}")
        if self.game_mode == "Reaction":
            if last_reaction is not None:
                self.last_reaction_label.configure(text=f"Last Reaction: {last_reaction * 1000:.0f} ms")
            if self.reaction_times:
                avg_time = sum(self.reaction_times) / len(self.reaction_times)
                self.avg_reaction_label.configure(text=f"Avg. Reaction: {avg_time * 1000:.0f} ms")