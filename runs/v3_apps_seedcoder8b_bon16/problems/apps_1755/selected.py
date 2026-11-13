import sys
from typing import List, Set

def min_operations_to_increasing(n: int, k: int, a: List[int], b: Set[int]) -> int:
    if k == 0:
        return sum(1 for i in range(1, n) if a[i] <= a[i-1])

    operations = 0
    last = float('-inf')
    for i in range(n):
        if i + 1 in b:
            if a[i] <= last:
                return -1
            last = a[i]
        else:
            if a[i] <= last:
                operations += 1
                a[i] = last + 1
            last = a[i]

    return operations

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = set(map(int, input().split())) if k > 0 else set()

    result = min_operations_to_increasing(n, k, a, b)
    print(result)

if __name__ == "__main__":
    main()