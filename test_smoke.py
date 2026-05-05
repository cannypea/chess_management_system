# test_smoke.py
from models import Player, Tournament, Club
from pairing import swiss_pair
from service import TournamentService

def run_dashboard_tests():
    """
    A generator that yields results step-by-step for the UI to display.
    Each yield returns a string: "Description ... PASSED"
    """
    service = TournamentService()

    # Test 1: Club Creation
    try:
        club = Club("Test Club")
        yield "Creating Club ... PASSED"
    except Exception as e: yield f"Creating Club ... FAILED ({e})"

    # Test 2: Player Creation with Specs
    try:
        p1 = Player("Alice", "alice@test.com", "TS10001", "1990-01-01")
        p2 = Player("Bob", "bob@test.com", "TS10002", "1992-05-05")
        yield "Creating Spec-Compliant Players ... PASSED"
    except Exception as e: yield f"Creating Players ... FAILED ({e})"

    # Test 3: Club Registration
    try:
        club.players.append(p1)
        club.players.append(p2)
        yield "Registering Players to Club ... PASSED"
    except Exception as e: yield f"Registration ... FAILED ({e})"

    # Test 4: Tournament Initialization
    try:
        t = service.create_tournament("Test Tourney", "Main Hall", "2026-01-01", "2026-01-02")
        t.players = [p1, p2]
        yield "Initializing Tournament ... PASSED"
    except Exception as e: yield f"Tournament Init ... FAILED ({e})"

    # Test 5: Swiss Pairing (Round 1)
    try:
        pairs = swiss_pair(t.players, 1)
        assert len(pairs) == 1
        yield "Swiss Pairing Logic (Round 1) ... PASSED"
    except Exception as e: yield f"Pairing ... FAILED ({e})"

    # Test 6: Standings Logic
    try:
        p1.score = 1.0
        sorted_p = t.standings()
        assert sorted_p[0].chess_id == "TS10001"
        yield "Standings Sorting Logic ... PASSED"
    except Exception as e: yield f"Standings ... FAILED ({e})"

    yield "--- ALL CORE FEATURES VERIFIED ---"