import random
import unittest

from models import Match, Player, Round
from pairing import swiss_pair
from rating import update_elo
from service import TournamentService


def play_full_tournament(tournament, rounds=4, seed=42):
    """Play a full tournament using deterministic match results."""
    random.seed(seed)
    result_patterns = [
        [(1.0, 0.0)],
        [(0.0, 1.0)],
        [(0.5, 0.5)],
        [(1.0, 0.0)],
    ]

    for round_number in range(1, rounds + 1):
        pairs = swiss_pair(tournament.players, round_number)
        rnd = Round(f"Round {round_number}")

        for pair_index, (p1, p2) in enumerate(pairs):
            # Reuse the same score pattern for each pairing in the round.
            s1, s2 = result_patterns[round_number - 1][0]
            match = Match(p1, p2)
            match.set_result(s1, s2)
            update_elo(p1, p2, s1, s2)
            rnd.matches.append(match)

        tournament.rounds.append(rnd)
        tournament.current_round = round_number

    tournament.completed = len(tournament.rounds) >= tournament.total_rounds


class TournamentFlowTest(unittest.TestCase):
    def test_create_and_play_tournament_from_start_to_finish(self):
        service = TournamentService()
        tournament = service.create_tournament(
            name="Flow Test Open",
            venue="Main Hall",
            start_date="2026-06-01",
            end_date="2026-06-04",
            total_rounds=4,
        )

        players = [
            Player("Alice", "alice@example.com", "TS10001", "1990-01-01"),
            Player("Bob", "bob@example.com", "TS10002", "1991-02-02"),
            Player("Charlie", "charlie@example.com", "TS10003", "1992-03-03"),
            Player("David", "david@example.com", "TS10004", "1993-04-04"),
            Player("Eve", "eve@example.com", "TS10005", "1994-05-05"),
            Player("Frank", "frank@example.com", "TS10006", "1995-06-06"),
        ]

        for player in players:
            tournament.add_player(player)

        play_full_tournament(tournament, rounds=4, seed=42)

        self.assertEqual(len(tournament.rounds), 4)
        self.assertEqual(tournament.current_round, 4)
        self.assertTrue(tournament.completed)

        self.assertTrue(all(len(rnd.matches) == len(players) // 2 for rnd in tournament.rounds))
        self.assertTrue(any(player.rating != 1200 for player in tournament.players))

        standings = tournament.standings()
        self.assertEqual(standings, sorted(tournament.players, key=lambda p: (-p.score, -p.rating)))
        self.assertGreaterEqual(standings[0].score, standings[-1].score)


if __name__ == "__main__":
    unittest.main()
