import os
import ttkbootstrap as ttk
from ui import App

# Constants for pathing as per specifications
BASE_DATA_PATH = "data"
CLUBS_PATH = os.path.join(BASE_DATA_PATH, "clubs")
TOURNAMENTS_PATH = os.path.join(BASE_DATA_PATH, "tournaments")


def initialize_folders():
    """
    Ensures the strict folder structure required by specs exists
    at runtime before the app starts.
    """
    folders = [BASE_DATA_PATH, CLUBS_PATH, TOURNAMENTS_PATH]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            print(f"Created directory: {folder}")


def run_app():
    # 1. Setup environment
    initialize_folders()

    # 2. Initialize the UI with a professional theme
    # 'flatly' or 'cosmo' are good choices for a clean, modular look
    root = ttk.Window(themename="flatly")

    root.title("♟ Castle Chess Manager")
    
    # Adjusted geometry to accommodate the new Tournament Dashboard requirements
    # (Player list, standings, and multi-round views)
    root.geometry("1100x700") 
    root.minsize(900, 600)

    # 3. Inject the root into the App controller
    # The App class in ui.py will handle the View switching logic
    App(root)

    # 4. Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    # Requirement: Started from the console
    run_app()