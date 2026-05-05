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

        return t