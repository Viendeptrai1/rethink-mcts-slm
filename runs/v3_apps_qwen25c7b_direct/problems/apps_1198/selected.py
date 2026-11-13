import sys
from typing import List

def min_partition_sum(a: List[int], c: int) -> int:
    n = len(a)
    total_sum = sum(a)
    sorted_a = sorted(a)
    
    result = float('inf')
    for i in range(c):
        result = min(result, total_sum - sum(sorted_a[:i]) - sum(sorted_a[n-c+i+1:n]))
    
    return result

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:]))
    
    print(min_partition_sum(a, c))