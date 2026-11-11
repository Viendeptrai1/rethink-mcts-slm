import sys

def calculate_wasted_votes_and_efficiency_gap(P, D, precincts):
    # Initialize district results
    district_results = {d: {'total_votes': 0, 'votes_A': 0, 'votes_B': 0} for d in range(1, D + 1)}
    
    # Aggregate votes by district
    for d, a, b in precincts:
        district_results[d]['total_votes'] += a + b
        district_results[d]['votes_A'] += a
        district_results[d]['votes_B'] += b
    
    # Calculate wasted votes and determine winners
    wasted_votes_A = 0
    wasted_votes_B = 0
    results = []
    
    for d in range(1, D + 1):
        total_votes = district_results[d]['total_votes']
        votes_A = district_results[d]['votes_A']
        votes_B = district_results[d]['votes_B']
        
        majority_votes_needed = (total_votes // 2) + 1
        
        if votes_A > votes_B:
            winner = 'A'
            wasted_votes_A += votes_A - majority_votes_needed
            wasted_votes_B += votes_B
        else:
            winner = 'B'
            wasted_votes_A += votes_A
            wasted_votes_B += votes_B - majority_votes_needed
        
        results.append((winner, wasted_votes_A, wasted_votes_B))
    
    # Calculate efficiency gap
    total_votes = sum(district_results[d]['total_votes'] for d in range(1, D + 1))
    efficiency_gap = abs(wasted_votes_A - wasted_votes_B) / total_votes
    
    return results, efficiency_gap

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    P = int(data[0])
    D = int(data[1])
    
    precincts = []
    index = 2
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