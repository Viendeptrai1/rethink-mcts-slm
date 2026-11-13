import sys

def calculate_efficiency_gap(P, D, precincts):
    results = []
    total_wasted_A = 0
    total_wasted_B = 0
    
    for d in range(1, D + 1):
        votes_A = 0
        votes_B = 0
        for p in precincts:
            if p[0] == d:
                votes_A += p[1]
                votes_B += p[2]
        
        total_votes = votes_A + votes_B
        needed_to_win = (total_votes // 2) + 1
        
        if votes_A > needed_to_win:
            winner = 'A'
            wasted_A = votes_A - needed_to_win
            wasted_B = votes_B
        else:
            winner = 'B'
            wasted_A = votes_A
            wasted_B = votes_B - needed_to_win
        
        results.append((winner, wasted_A, wasted_B))
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B
    
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / P
    return results, efficiency_gap

if __name__ == "__main__":
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
    
    results, efficiency_gap = calculate_efficiency_gap(P, D, precincts)
    
    for result in results:
        print(result[0], result[1], result[2])
    
    print(efficiency_gap)