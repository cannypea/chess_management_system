def calculate_expected_score(rating_a, rating_b):
    """
    Calculates the expected score of player A against player B.
    Formula: 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    """
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_elo(p1, p2, s1, s2, k=32):
    """
    Updates the ratings of two players based on match results.
    
    Technical Specs Requirement:
    - Winner gets 1 point.
    - Loser gets 0 points.
    - Tie gets 0.5 points.
    """
    # Calculate expectations
    expected_1 = calculate_expected_score(p1.rating, p2.rating)
    expected_2 = calculate_expected_score(p2.rating, p1.rating)

    # Calculate new ratings
    # We use round() to keep ratings as clean integers if preferred, 
    # though floats are more precise for Swiss pairing tie-breaks.
    p1.rating += k * (s1 - expected_1)
    p2.rating += k * (s2 - expected_2)
    
    # Optional: Ensure ratings don't drop below a floor (e.g., 100)
    p1.rating = max(100, p1.rating)
    p2.rating = max(100, p2.rating)