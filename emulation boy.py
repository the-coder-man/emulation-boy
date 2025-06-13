import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from pyboy import PyBoy

class EmulatorLauncher:
    def __init__(self, master):
        self.master = master
        self.master.title("emulation_boy.exe")
        self.master.geometry("400x300")
        self.label = tk.Label(master, text="Select a Game ROM file:")
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(master, text="Upload a GB, GBC, GBA game file.", command=self.upload_rom)
        self.upload_btn.pack(pady=10)

        self.rom_path = None

    def upload_rom(self):
        filepath = filedialog.askopenfilename(filetypes=[
        ])
        if not filepath:
            return

        self.rom_path = filepath
        ext = os.path.splitext(filepath)[1].lower()

        if ext in [".gb", ".gbc"]:
            self.run_gameboy_rom(filepath)
        elif ext in [".gba"]:
            self.run_mgba(filepath)
            
        else:
            messagebox.showerror("Unsupported Format", f"Unsupported file type: {ext}")

    def run_gameboy_rom(self, filepath):
        try:
            pyboy = PyBoy(filepath)
            while pyboy.tick():
                pass
            pyboy.stop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Game Boy ROM: {e}")

    def run_mgba(self, filepath): 
        try:
            subprocess.run(["mGBA.app/Contents/MacOS/mGBA", filepath], check=True)
        except FileNotFoundError:
            messagebox.showerror("Error", "mGBA not found. Make sure it is installed and added to your system PATH.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"mGBA failed to run. {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorLauncher(root)
    root.mainloop()
