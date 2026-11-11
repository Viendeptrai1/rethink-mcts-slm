import sys
from typing import List

def max_students_to_lunch(n: int, group_sizes: List[int], k: int, x: int, a: int, b: int) -> int:
    total_lunches = k * x
    group_sizes.sort(reverse=True)
    
    def can_take_lunch(num_students: int) -> bool:
        lunches_needed = 0
        for size in group_sizes:
            if num_students >= size:
                lunches_needed += size
                num_students -= size
            else:
                return False
        return lunches_needed <= total_lunches
    
    max_students = -1
    for num_students in range(a, min(b + 1, sum(group_sizes) + 1)):
        if can_take_lunch(num_students):
            max_students = num_students
    
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