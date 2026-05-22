from models import Tournament, Player, Round, Match


class TournamentService:
    def create_tournament(self, name, venue, start_date, end_date, total_rounds=4):
        """Creates a new Tournament instance with mandatory spec fields."""
        return Tournament(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            total_rounds=total_rounds
        )

    # ---------------- SAFE REBUILD ENGINE ----------------

    def rebuild_tournament(self, data):
        """
        Rebuilds a full Tournament object from JSON data.
        Requirement: Ensures in-memory objects are in sync with JSON files.
        """
        # 1. Rebuild basic Tournament attributes
        t = Tournament(
            name=data["name"],
            venue=data.get("venue", "N/A"),
            start_date=data.get("start_date", "N/A"),
            end_date=data.get("end_date", "N/A"),
            total_rounds=data.get("total_rounds", 4),
            current_round=data.get("current_round", 1),
            completed=data.get("completed", False)
        )
        t.id = data.get("id", t.id)

        # 2. Rebuild Players (Using chess_id as the primary map key per specs)
        players_map = {}
        for p_data in data.get("players", []):
            p = Player.from_dict(p_data)
            players_map[p.chess_id] = p
            t.players.append(p)

        # 3. Rebuild Rounds & Matches
        for r_data in data.get("rounds", []):
            rnd = Round(r_data["name"])

            for m_data in r_data.get("matches", []):
                # Retrieve player instances by their Chess IDs saved in JSON
                p1 = players_map.get(m_data.get("p1_id"))
                p2 = players_map.get(m_data.get("p2_id"))

                if p1 and p2:
                    match = Match(p1, p2)
                    # We assign scores directly to avoid calling set_result() 
                    # during rebuild, which would double-count the scores.
                    match.s1 = m_data.get("s1")
                    match.s2 = m_data.get("s2")
                    match.id = m_data.get("id", match.id)
                    rnd.matches.append(match)

            t.rounds.append(rnd)

        # After rebuilding rounds/matches, recompute player scores and ratings
        # from the match history to ensure the UI reflects ratings derived
        # from game results (prevents stale or inconsistent rating values).
        self._recompute_from_history(t)

        return t

    def _recompute_from_history(self, tournament: Tournament, baseline_rating: int = 1200):
        """Recompute player scores, opponents and Elo ratings from stored match history.

        This resets each player's `score` and `opponents` and sets `rating` to
        `baseline_rating` before replaying rounds in order and applying
        `Match` results with `update_elo` to derive the current ratings.
        """
        # Defensive: ensure players exist
        if not tournament.players:
            return

        # Reset players
        for p in tournament.players:
            p.score = 0.0
            p.opponents = set()
            p.rating = baseline_rating

        # Replay rounds and matches in order
        from rating import update_elo

        for rnd in tournament.rounds:
            for m in rnd.matches:
                # Only apply matches that have explicit scores
                if getattr(m, "s1", None) is None or getattr(m, "s2", None) is None:
                    continue

                # Ensure players are the tournament instances
                p1 = next((pl for pl in tournament.players if pl.chess_id == m.p1.chess_id), m.p1)
                p2 = next((pl for pl in tournament.players if pl.chess_id == m.p2.chess_id), m.p2)

                # Apply scores and opponent history
                p1.score += m.s1
                p2.score += m.s2
                p1.opponents.add(p2.chess_id)
                p2.opponents.add(p1.chess_id)

                # Update Elo based on this match result
                update_elo(p1, p2, m.s1, m.s2)