def calculate_efficiency_gap():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    P = int(data[0])
    D = int(data[1])
    
    index = 2
    district_votes = [0] * (D + 1)
    party_a_votes = [0] * (D + 1)
    party_b_votes = [0] * (D + 1)
    
    for _ in range(P):
        d_i = int(data[index])
        a_i = int(data[index + 1])
        b_i = int(data[index + 2])
        
        district_votes[d_i] += a_i + b_i
        party_a_votes[d_i] += a_i
        party_b_votes[d_i] += b_i
        
        index += 3
    
    total_votes = sum(district_votes)
    total_wasted_a = 0
    total_wasted_b = 0
    
    for d in range(1, D + 1):
        votes_for_a = party_a_votes[d]
        votes_for_b = party_b_votes[d]
        
        if votes_for_a > votes_for_b:
            wasted_a = votes_for_a - (district_votes[d] // 2 + 1)
            wasted_b = votes_for_b
        else:
            wasted_a = votes_for_a
            wasted_b = votes_for_b - (district_votes[d] // 2 + 1)
        
        total_wasted_a += max(0, wasted_a)
        total_wasted_b += max(0, wasted_b)
        
        if votes_for_a > votes_for_b:
            print("A", wasted_a, wasted_b)
        else:
            print("B", wasted_a, wasted_b)
    
    efficiency_gap = abs(total_wasted_a - total_wasted_b) / total_votes
    print(f"{efficiency_gap:.10f}")