def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    P, D = map(int, data[0].split())
    precincts = [tuple(map(int, line.split())) for line in data[1:P+1]]
    
    district_totals = {}
    
    for district, a_votes, b_votes in precincts:
        if district not in district_totals:
            district_totals[district] = (0, 0)
        district_totals[district] = (
            district_totals[district][0] + a_votes,
            district_totals[district][1] + b_votes
        )
    
    total_votes = 0
    total_wasted_A = 0
    total_wasted_B = 0
    
    for district in range(1, D + 1):
        a_votes, b_votes = district_totals[district]
        total_votes += a_votes + b_votes
        
        if a_votes > b_votes:
            winner = 'A'
            wasted_A = 0
            wasted_B = b_votes
        else:
            winner = 'B'
            wasted_A = a_votes
            wasted_B = 0
        
        # Calculate wasted votes
        V = a_votes + b_votes
        strict_majority = (V // 2) + 1
        
        if winner == 'A':
            excess_votes = max(0, a_votes - strict_majority)
            wasted_A = excess_votes
            wasted_B = b_votes
        else:
            excess_votes = max(0, b_votes - strict_majority)
            wasted_B = excess_votes
            wasted_A = a_votes
        
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B
        
        print(f"{winner} {wasted_A} {wasted_B}")
    
    # Calculate efficiency gap
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / total_votes
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    main()