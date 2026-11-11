import sys
from typing import List

def max_calm_group_sum(n: int, a: List[int], b: List[int]) -> int:
    # Sort students by their skill levels in descending order
    students = sorted(zip(a, b), key=lambda x: x[1], reverse=True)
    
    max_sum = 0
    
    # Iterate over all pairs of students
    for i in range(n):
        for j in range(i + 1, n):
            a_i, b_i = students[i]
            a_j, b_j = students[j]
            
            # Check if they can work together calmly
            if (a_i & a_j) == a_i and (a_i & a_j) == a_j:
                max_sum = max(max_sum, b_i + b_j)
    
    return max_sum

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    b = list(map(int, data[n+1:2*n+1]))
    
    result = max_calm_group_sum(n, a, b)
    print(result)

if __name__ == "__main__":
    main()