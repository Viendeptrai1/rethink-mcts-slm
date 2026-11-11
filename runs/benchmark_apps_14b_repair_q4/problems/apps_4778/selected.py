import sys

def calculate_wasted_votes_and_efficiency_gap(P, D, precincts):
    districts = {d: {'A': 0, 'B': 0} for d in range(1, D + 1)}
    
    for d, a, b in precincts:
        districts[d]['A'] += a
        districts[d]['B'] += b
    
    total_votes = sum(a + b for _, a, b in precincts)
    total_wasted_A = 0
    total_wasted_B = 0
    
    results = []
    
    for d in range(1, D + 1):
        a_votes = districts[d]['A']
        b_votes = districts[d]['B']
        
        if a_votes > b_votes:
            winner = 'A'
            majority_votes_needed = (a_votes + b_votes) // 2 + 1
            wasted_A = max(0, a_votes - majority_votes_needed)
            wasted_B = b_votes
        else:
            winner = 'B'
            majority_votes_needed = (a_votes + b_votes) // 2 + 1
            wasted_A = a_votes
            wasted_B = max(0, b_votes - majority_votes_needed)
        
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B
        results.append((winner, wasted_A, wasted_B))
    
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / total_votes
    
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