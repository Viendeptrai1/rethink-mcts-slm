import sys

def calculate_wasted_votes_and_efficiency_gap(P, D, precincts):
    # Initialize data structures
    district_votes = [{} for _ in range(D)]
    total_wasted_A = 0
    total_wasted_B = 0
    
    # Tally votes for each district
    for d, a, b in precincts:
        if 'A' in district_votes[d-1]:
            district_votes[d-1]['A'] += a
            district_votes[d-1]['B'] += b
        else:
            district_votes[d-1]['A'] = a
            district_votes[d-1]['B'] = b
    
    # Calculate wasted votes for each district
    results = []
    for votes in district_votes:
        total_votes = votes['A'] + votes['B']
        majority_votes_needed = total_votes // 2 + 1
        
        if votes['A'] > votes['B']:
            wasted_A = votes['A'] - majority_votes_needed
            wasted_B = votes['B']
            winner = 'A'
        else:
            wasted_A = votes['A']
            wasted_B = votes['B'] - majority_votes_needed
            winner = 'B'
        
        results.append((winner, wasted_A, wasted_B))
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B
    
    # Calculate efficiency gap
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / sum(votes['A'] + votes['B'] for votes in district_votes)
    
    return results, efficiency_gap

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    P = int(data[index])
    D = int(data[index + 1])
    index += 2
    
    precincts = []
    for _ in range(P):
        d = int(data[index])
        a = int(data[index + 1])
        b = int(data[index + 2])
        precincts.append((d, a, b))
        index += 3
    
    results, efficiency_gap = calculate_wasted_votes_and_efficiency_gap(P, D, precincts)
    
    for result in results:
        print(result[0], result[1], result[2])
    
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    main()