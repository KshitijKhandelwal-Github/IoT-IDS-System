# visualizer.py
import tkinter as tk
from tkinter import font
import os
import time

# --- CONFIGURATION ---
ATTACK_LOG_FILE = 'logs/attack.log'
COORDINATION_FILE = 'coordination.log'
POLL_INTERVAL_MS = 1000  # 1 second

# --- GUI APPLICATION CLASS ---
class NetVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Honeynet Visualizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.log_font = font.Font(family="Courier", size=10)

        # To track new log entries
        self.last_log_size = 0

        self.setup_ui()
        self.update_status() # Start the update loop

    def setup_ui(self):
        # Canvas for topology
        self.canvas = tk.Canvas(self.root, bg="#1C1C1C", highlightthickness=0)
        self.canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.5)

        # Log display
        log_frame = tk.Frame(self.root, bg="#2E2E2E")
        log_frame.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.35)
        
        log_title = tk.Label(log_frame, text="Live Attack Log", font=self.title_font, fg="#FFFFFF", bg="#2E2E2E")
        log_title.pack(anchor="w")

        self.log_text = tk.Text(log_frame, bg="#000000", fg="#00FF00", font=self.log_font, wrap=tk.WORD, borderwidth=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.draw_topology()

    def draw_topology(self):
        """Draws the static network diagram."""
        # --- Devices ---
        # Attacker
        self.canvas.create_rectangle(50, 100, 150, 200, fill="#4A4A4A", outline="#7F7F7F")
        self.canvas.create_text(100, 150, text="Attacker\nh1", fill="white", font=self.label_font)
        
        # Smart Plug
        self.plug_rect = self.canvas.create_rectangle(325, 100, 425, 200, fill="#4A4A4A", outline="#7F7F7F")
        self.canvas.create_text(375, 150, text="Smart Plug\nh2", fill="white", font=self.label_font)
        self.plug_status_light = self.canvas.create_oval(400, 105, 420, 125, fill="gray", outline="")

        # Camera
        self.cam_rect = self.canvas.create_rectangle(600, 100, 700, 200, fill="#4A4A4A", outline="#7F7F7F")
        self.canvas.create_text(650, 150, text="Camera\nh3", fill="white", font=self.label_font)
        self.cam_status_light = self.canvas.create_oval(675, 105, 695, 125, fill="gray", outline="")

        # --- Switch & Links ---
        self.canvas.create_rectangle(350, 250, 400, 300, fill="#003366", outline="#0055AA")
        self.canvas.create_text(375, 275, text="s1", fill="white")
        
        self.canvas.create_line(100, 200, 375, 250, fill="white", width=2) # Attacker -> Switch
        self.canvas.create_line(375, 200, 375, 250, fill="white", width=2) # Plug -> Switch
        self.canvas.create_line(650, 200, 375, 250, fill="white", width=2) # Camera -> Switch

    def update_status(self):
        """Periodically reads log files and updates the GUI."""
        # --- Update Device Status Lights ---
        power_state = "OFF"
        if os.path.exists(COORDINATION_FILE):
            with open(COORDINATION_FILE, 'r') as f:
                for line in f:
                    if "plug_1_power:ON" in line:
                        power_state = "ON"
        
        if power_state == "ON":
            self.canvas.itemconfig(self.plug_status_light, fill="green")
            self.canvas.itemconfig(self.cam_status_light, fill="green")
        else:
            self.canvas.itemconfig(self.plug_status_light, fill="red")
            self.canvas.itemconfig(self.cam_status_light, fill="red")
            
        # --- Update Live Log ---
        if os.path.exists(ATTACK_LOG_FILE):
            current_size = os.path.getsize(ATTACK_LOG_FILE)
            if current_size > self.last_log_size:
                with open(ATTACK_LOG_FILE, 'r') as f:
                    f.seek(self.last_log_size)
                    new_logs = f.read()
                    self.log_text.insert(tk.END, new_logs)
                    self.log_text.see(tk.END) # Auto-scroll
                self.last_log_size = current_size

        # Schedule the next update
        self.root.after(POLL_INTERVAL_MS, self.update_status)

if __name__ == '__main__':
    window = tk.Tk()
    app = NetVisualizer(window)
    window.mainloop()
