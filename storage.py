import json
import os

# Define the base structure to match your App class and Technical Specs
DATA_DIR = "data"
TOURNAMENT_DIR = os.path.join(DATA_DIR, "tournaments")
CLUB_DIR = os.path.join(DATA_DIR, "clubs")
CLUB_FILE = os.path.join(CLUB_DIR, "clubs.json")

# Ensure the strict folder structure exists at initialization
os.makedirs(TOURNAMENT_DIR, exist_ok=True)
os.makedirs(CLUB_DIR, exist_ok=True)

# ======================================================
# TOURNAMENT STORAGE
# ======================================================

def save(name, data):
    """Save tournament data as JSON in the tournaments subfolder."""
    clean_name = os.path.basename(name).replace(".json", "")
    path = os.path.join(TOURNAMENT_DIR, f"{clean_name}.json")

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[SAVE ERROR] {path}: {e}")


def load(name):
    """Load tournament data safely from the tournaments subfolder."""
    clean_name = os.path.basename(name).replace(".json", "")
    path = os.path.join(TOURNAMENT_DIR, f"{clean_name}.json")

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[LOAD ERROR] {path}: {e}")
        return None


def list_tournaments():
    """List saved tournaments from the correct subfolder."""
    try:
        files = os.listdir(TOURNAMENT_DIR)
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
    except Exception as e:
        print("[LIST ERROR]", e)
        return []


# ======================================================
# CLUB STORAGE
# ======================================================

def save_clubs(clubs):
    """
    Saves a list of Club objects to data/clubs/clubs.json.
    Requirement: Each club must include its registered players.
    """
    try:
        data = []
        for c in clubs:
            # Map the club and its nested player objects to a dictionary
            club_dict = {
                "id": getattr(c, "id", None),
                "name": getattr(c, "name", "Unnamed Club"),
                "players": [p.to_dict() for p in getattr(c, "players", [])]
            }
            data.append(club_dict)

        with open(CLUB_FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"[SAVE CLUBS ERROR] {CLUB_FILE}: {e}")


def load_clubs():
    """
    Returns RAW data from data/clubs/clubs.json.
    This data is used by the App/Service to rebuild Player instances.
    """
    if not os.path.exists(CLUB_FILE):
        return []

    try:
        with open(CLUB_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[LOAD CLUBS ERROR] {CLUB_FILE}: {e}")
        return []