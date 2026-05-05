import random

def swiss_pair(players, round_number):
    """
    Generates pairings based on the tournament round.
    Round 1: Random pairings.
    Subsequent Rounds: Swiss System (score-based).
    """
    # Defensive check: ensure we have an even number of players
    # If odd, the technical specs don't specify a 'bye', 
    # but we should handle it or ensure the UI prevents it.
    active_players = list(players)
    
    if round_number == 1:
        # Technical Spec: "The pairings for the first round are generated randomly."
        random.shuffle(active_players)
    else:
        # Technical Spec: "Subsequent rounds are dynamically generated based on results."
        # Primary sort: Score (Descending)
        # Secondary sort: Rating (Descending)
        active_players.sort(key=lambda x: (-x.score, -x.rating))

    pairs = []
    used_ids = set()

    for i, p1 in enumerate(active_players):
        if p1.chess_id in used_ids:
            continue

        # Look for the next available opponent
        found_opponent = False
        for p2 in active_players[i + 1:]:
            if p2.chess_id in used_ids:
                continue
            
            # Technical Spec: Ensure they haven't played each other before
            if p2.chess_id in p1.opponents:
                continue

            # Found a valid match
            pairs.append((p1, p2))
            used_ids.add(p1.chess_id)
            used_ids.add(p2.chess_id)
            found_opponent = True
            break
            
        # Fallback: If no valid opponent is found (everyone played everyone),
        # pair with the next available player regardless of history to avoid a crash.
        if not found_opponent and p1.chess_id not in used_ids:
            for p2 in active_players[i + 1:]:
                if p2.chess_id not in used_ids:
                    pairs.append((p1, p2))
                    used_ids.add(p1.chess_id)
                    used_ids.add(p2.chess_id)
                    break

    return pairs