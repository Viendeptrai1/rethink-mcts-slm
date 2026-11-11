import sys
from typing import List

def max_students_to_lunch(n: int, group_sizes: List[int], k: int, x: int, a: int, b: int) -> int:
    total_lunches = k * x
    dp = [[False] * (total_lunches + 1) for _ in range(b + 1)]
    dp[0][0] = True
    
    for group_size in group_sizes:
        new_dp = [row[:] for row in dp]
        for students in range(b, -1, -1):
            for lunches in range(total_lunches, -1, -1):
                if dp[students][lunches]:
                    if students + group_size <= b:
                        new_dp[students + group_size][lunches + group_size] = True
        dp = new_dp
    
    max_students = -1
    for students in range(a, b + 1):
        for lunches in range(total_lunches + 1):
            if dp[students][lunches] and lunches % x == 0:
                max_students = max(max_students, students)
    
    return max_students if max_students != -1 else "impossible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    group_sizes = list(map(int, data[1:n+1]))
    k = int(data[n+1])
    x = int(data[n+2])
    a = int(data[n+3])
    b = int(data[n+4])
    
    result = max_students_to_lunch(n, group_sizes, k, x, a, b)
    print(result)

if __name__ == "__main__":
    main()