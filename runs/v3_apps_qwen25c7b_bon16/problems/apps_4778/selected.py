import sys
from typing import List, Tuple

def calculate_efficiency_gap(lost_votes_a: int, lost_votes_b: int, total_votes: int) -> float:
    return abs(lost_votes_a - lost_votes_b) / total_votes

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    P = int(data[index])
    D = int(data[index + 1])
    index += 2
    
    precincts = []
    for _ in range(P):
        d = int(data[index]) - 1
        a = int(data[index + 1])
        b = int(data[index + 2])
        precincts.append((d, a, b))
        index += 3
    
    district_results = []
    total_lost_votes_a = 0
    total_lost_votes_b = 0
    total_votes = sum(a + b for _, a, b in precincts)
    
    for d in range(D):
        votes_for_a = 0
        votes_for_b = 0
        for p in precincts:
            if p[0] == d:
                votes_for_a += p[1]
                votes_for_b += p[2]
        
        needed_to_win = (votes_for_a + votes_for_b) // 2 + 1
        
        if votes_for_a > needed_to_win:
            won_by_a = True
            lost_votes_a = votes_for_a - needed_to_win
            lost_votes_b = votes_for_b
        else:
            won_by_a = False
            lost_votes_a = votes_for_a
            lost_votes_b = votes_for_b - needed_to_win
        
        district_results.append(('A' if won_by_a else 'B', lost_votes_a, lost_votes_b))
        total_lost_votes_a += lost_votes_a
        total_lost_votes_b += lost_votes_b
    
    for result in district_results:
        print(result[0], result[1], result[2])
    
    efficiency_gap = calculate_efficiency_gap(total_lost_votes_a, total_lost_votes_b, total_votes)
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    main()