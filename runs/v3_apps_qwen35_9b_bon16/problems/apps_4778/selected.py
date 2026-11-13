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

    # Data structures to accumulate votes per district
    # districts will be a list of size D+1 (using 1-based indexing for convenience)
    # Each entry will be a dictionary or tuple: { 'A': votes_A, 'B': votes_B }
    districts = [None] * (D + 1)

    for _ in range(P):
        d = int(next(iterator))
        a = int(next(iterator))
        b = int(next(iterator))

        if districts[d] is None:
            districts[d] = {'A': 0, 'B': 0}
        districts[d]['A'] += a
        districts[d]['B'] += b

    total_wasted_A = 0
    total_wasted_B = 0
    district_output_lines = []

    for d in range(1, D + 1):
        votes_A = districts[d]['A']
        votes_B = districts[d]['B']
        total_votes = votes_A + votes_B

        majority_threshold = (total_votes // 2) + 1

        if votes_A > votes_B:
            # Party A wins
            wasted_A = max(0, votes_A - majority_threshold)
            wasted_B = votes_B  # All votes for the loser are wasted
            winner = 'A'
        else:
            # Party B wins (guaranteed no ties by problem statement)
            wasted_B = max(0, votes_B - majority_threshold)
            wasted_A = votes_A  # All votes for the loser are wasted
            winner = 'B'

        total_wasted_A += wasted_A
        total_wasted_B += wasted_B

        district_output_lines.append(f"{winner} {wasted_A} {wasted_B}")

    # Calculate efficiency gap
    V = sum(d['A'] + d['B'] for d in districts[1:])
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / V

    # Print results
    for line in district_output_lines:
        print(line)
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    solve()