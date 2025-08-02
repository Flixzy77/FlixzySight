# 🎯 FlixzySight – Crosshair Overlay & Aim Trainer

FlixzySight is a modern desktop application for gamers that allows you to create, modify, and overlay crosshairs in your games, as well as train your aim. The application combines the convenience of a graphical editor, practical presets, and a training system for FPS players.

## ✅ Key Features:

### 🔹 1. Crosshair Overlay
- The crosshair is displayed in the center of the screen as a transparent overlay (always on top).
- Ability to toggle on/off with a hotkey (e.g., F8).
- Works independently of the game (compatible with most windowed and borderless fullscreen games).

### 🎨 2. Advanced Crosshair Editor
- Pixel editing mode (grid) - brush, eraser, lines.
- Import crosshair from PNG / export to PNG.
- Color, thickness, and transparency selection.
- Live preview of the crosshair on the overlay.
- Undo/redo, helper grid, zoom functionality.

### 📁 3. Presets
- Built-in ready-to-use presets (FPS, Retro, Circle, Dot, Cross, Green Dot, Valorant style, CS2).
- Ability to save your own custom presets.
- Export/import presets (.crossx.json or .png).

### 🧠 4. Aim Trainer
- Built-in training modes: Reaction, Speed, Precision.
- Statistics: average reaction time, accuracy %, hits per minute.
- Display modes: Light/Dark mode.

### ⚙️ 5. Settings
- Configure the hotkey to toggle the overlay.
- Option to automatically start with the system.
- GUI theme selection (Dark / Light).

### 🕘 6. Changelog
- A dedicated tab in the GUI with the application's version history.

### 🧩 7. Modern GUI
- Sidebar for easy navigation.
- Modern style (dark mode, rounded corners, shadows).
- Intuitive section switching without reloading.

## 🚀 How to Run

1.  **Clone or download the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python run.py
    ```