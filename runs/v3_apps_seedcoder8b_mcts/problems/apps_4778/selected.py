def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    P = int(data[0])
    D = int(data[1])
    
    index = 2
    precincts = []
    
    for _ in range(P):
        d_i = int(data[index])
        a_i = int(data[index + 1])
        b_i = int(data[index + 2])
        precincts.append((d_i, a_i, b_i))
        index += 3
    
    district_votes = [{'A': 0, 'B': 0} for _ in range(D)]
    
    for d_i, a_i, b_i in precincts:
        district_votes[d_i - 1]['A'] += a_i
        district_votes[d_i - 1]['B'] += b_i
    
    total_votes = 0
    total_waste_A = 0
    total_waste_B = 0
    
    for district in district_votes:
        votes_A = district['A']
        votes_B = district['B']
        total_votes += votes_A + votes_B
        
        if votes_A > votes_B:
            winner = 'A'
            wasted_A = votes_A - (votes_A - votes_B)
            wasted_B = votes_B
        else:
            winner = 'B'
            wasted_A = votes_A
            wasted_B = votes_B - (votes_B - votes_A)
        
        print(winner, wasted_A, wasted_B)
        
        total_waste_A += wasted_A
        total_waste_B += wasted_B
    
    efficiency_gap = abs(total_waste_A - total_waste_B) / total_votes
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    main()