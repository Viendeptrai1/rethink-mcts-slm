import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    P = int(data[index])
    D = int(data[index + 1])
    index += 2
    
    precincts = []
    for _ in range(P):
        district = int(data[index])
        a_votes = int(data[index + 1])
        b_votes = int(data[index + 2])
        precincts.append((district, a_votes, b_votes))
        index += 3
    
    results = []
    total_wasted_A = 0
    total_wasted_B = 0
    
    for district in range(1, D + 1):
        a_total = 0
        b_total = 0
        for precinct in precincts:
            if precinct[0] == district:
                a_total += precinct[1]
                b_total += precinct[2]
        
        if a_total > b_total:
            winner = 'A'
            wasted_A = a_total - (b_total + (b_total + 1) // 2)
            wasted_B = b_total
        else:
            winner = 'B'
            wasted_A = a_total
            wasted_B = b_total - (a_total + (a_total + 1) // 2)
        
        results.append((winner, wasted_A, wasted_B))
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B
    
    total_votes = sum(a + b for _, a, b in precincts)
    efficiency_gap = abs(total_wasted_A - total_wasted_B) / total_votes
    
    for result in results:
        print(result[0], result[1], result[2])
    
    print(efficiency_gap)

if __name__ == "__main__":
    main()