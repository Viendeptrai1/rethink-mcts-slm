import sys
from typing import List

def can_split(difficulties: List[int], k: int, max_difficulty: int) -> bool:
    current_max = 0
    days_needed = 1
    
    for difficulty in difficulties:
        current_max = max(current_max, difficulty)
        if current_max > max_difficulty:
            days_needed += 1
            current_max = difficulty
            if days_needed > k:
                return False
    
    return True

def find_max_profit(n: int, k: int, difficulties: List[int]) -> (int, List[int]):
    left, right = 1, 2000
    while left < right:
        mid = (left + right + 1) // 2
        if can_split(difficulties, k, mid):
            left = mid
        else:
            right = mid - 1
    
    max_difficulty = left
    current_max = 0
    days_needed = 1
    distribution = []
    
    for difficulty in difficulties:
        current_max = max(current_max, difficulty)
        if current_max > max_difficulty:
            distribution.append(days_needed)
            days_needed = 1
            current_max = difficulty
        else:
            days_needed += 1
    
    distribution.append(days_needed)
    
    return max_difficulty * k, distribution

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    max_profit, distribution = find_max_profit(n, k, difficulties)
    
    print(max_profit)
    print(' '.join(map(str, distribution)))

if __name__ == "__main__":
    main()