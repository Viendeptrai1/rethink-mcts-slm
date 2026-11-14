import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        P = int(next(iterator))
        D = int(next(iterator))
    except StopIteration:
        return

    # Initialize data structures for each district
    # We need to store votes for A and B for each district
    # Districts are 1-indexed, so we'll use size D+1
    district_a_votes = [0] * (D + 1)
    district_b_votes = [0] * (D + 1)

    # Read P precincts
    for _ in range(P):
        d = int(next(iterator))
        a = int(next(iterator))
        b = int(next(iterator))
        
        district_a_votes[d] += a
        district_b_votes[d] += b

    total_votes = 0
    total_wasted_a = 0
    total_wasted_b = 0

    # Process each district
    for d in range(1, D + 1):
        votes_a = district_a_votes[d]
        votes_b = district_b_votes[d]
        district_total = votes_a + votes_b
        
        total_votes += district_total

        # Determine winner
        if votes_a > votes_b:
            winner = 'A'
            loser_votes = votes_b
            winner_votes = votes_a
        else:
            winner = 'B'
            loser_votes = votes_a
            winner_votes = votes_b

        # Calculate wasted votes
        # Lost votes: all votes for the losing candidate
        lost_votes = loser_votes
        
        # Excess votes: votes for the winner beyond floor(total/2) + 1
        # The threshold to win is floor(V/2) + 1
        threshold = (district_total // 2) + 1
        excess_votes = max(0, winner_votes - threshold)
        
        wasted_a = 0
        wasted_b = 0
        
        if winner == 'A':
            wasted_a = excess_votes
            wasted_b = lost_votes
        else:
            wasted_a = lost_votes
            wasted_b = excess_votes
        
        total_wasted_a += wasted_a
        total_wasted_b += wasted_b

        print(f"{winner} {wasted_a} {wasted_b}")

    # Calculate efficiency gap
    # E = |wA - wB| / V
    efficiency_gap = abs(total_wasted_a - total_wasted_b) / total_votes
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    solve()