import random
from models import Player, Tournament, Match, Round
from pairing import swiss_pair
from rating import update_elo


def create_test_tournament():
    """Creates a tournament with spec-compliant players and metadata."""
    t = Tournament(
        name="Test Open 2026",
        venue="Grand Hall",
        start_date="2026-05-01",
        end_date="2026-05-03"
    )

    # Specs require: Name, Email, Chess ID, Birthdate
    test_data = [
        ("Alice", "AB12345"),
        ("Bob", "CD67890"),
        ("Charlie", "EF11223"),
        ("David", "GH44556"),
        ("Eve", "IJ77889"),
        ("Frank", "KL00112")
    ]

    for name, chess_id in test_data:
        p = Player(
            name=name,
            email=f"{name.lower()}@example.com",
            chess_id=chess_id,
            birthdate="1990-01-01"
        )
        t.add_player(p)

    return t


def simulate_round(tournament):
    """Simulates a round using the required Swiss pairing logic."""
    round_num = len(tournament.rounds) + 1
    print(f"\n🎯 Running Round {round_num}...")

    # Updated pairing call to include round_number for spec compliance
    pairs = swiss_pair(tournament.players, round_num)
    rnd = Round(f"Round {round_num}")

    for p1, p2 in pairs:
        # Generate results: 1, 0, or 0.5 (Requirement compliance)
        s1 = random.choice([1, 0.5, 0])
        s2 = 1.0 - s1

        match = Match(p1, p2)
        match.set_result(s1, s2)

        # Update Elo using the rating service
        update_elo(p1, p2, s1, s2)

        rnd.matches.append(match)
        print(f"[{p1.chess_id}] {p1.name} vs [{p2.chess_id}] {p2.name} -> {s1}:{s2}")

    tournament.rounds.append(rnd)


def show_standings(tournament):
    """Displays standings sorted by score then rating."""
    print("\n📊 Standings:")
    # tournament.standings() handles the sorting logic internally
    for i, p in enumerate(tournament.standings(), 1):
        print(f"{i}. {p.name} ({p.chess_id}): Score={p.score}, Elo={round(p.rating, 1)}")


def run_test_simulation():
    t = create_test_tournament()

    # Simulate 3 rounds to test Swiss progression
    for _ in range(3):
        simulate_round(t)
        show_standings(t)

    print("\n✅ SIMULATION COMPLETE")


if __name__ == "__main__":
    run_test_simulation();