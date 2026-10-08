import sys
from typing import List

def max_students_to_lunch(n: int, groups: List[int], k: int, x: int, a: int, b: int) -> int:
    # Calculate the total number of lunches available
    total_lunches = k * x
    
    # Sort groups in descending order to try to maximize the number of students taken to lunch
    groups.sort(reverse=True)
    
    # Initialize the maximum number of students that can be taken to lunch
    max_students = 0
    
    # Try all possible subsets of groups
    from itertools import combinations
    for r in range(1, n + 1):
        for combo in combinations(groups, r):
            total_size = sum(combo)
            if a <= total_size <= b and total_size % x == 0 and total_size <= total_lunches:
                max_students = max(max_students, total_size)
    
    return max_students if max_students >= a else "impossible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    groups = list(map(int, data[1:n+1]))
    k = int(data[n+1])
    x = int(data[n+2])
    a = int(data[n+3])
    b = int(data[n+4])
    
    result = max_students_to_lunch(n, groups, k, x, a, b)
    print(result)

if __name__ == "__main__":
    main()