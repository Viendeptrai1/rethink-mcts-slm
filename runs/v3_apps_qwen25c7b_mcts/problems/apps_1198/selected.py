import sys
from typing import List

def min_partition_sum(a: List[int], c: int) -> int:
    a.sort(reverse=True)
    total_sum = 0
    n = len(a)
    
    for i in range(0, n, c):
        partition_size = min(c, n - i)
        partition_sum = sum(a[i:i+partition_size]) - sum(sorted(a[i:i+partition_size])[:partition_size // c])
        total_sum += partition_sum
    
    return total_sum

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:]))
    
    result = min_partition_sum(a, c)
    print(result)