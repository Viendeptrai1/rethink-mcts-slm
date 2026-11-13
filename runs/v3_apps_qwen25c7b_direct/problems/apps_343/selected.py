import sys
from typing import List

def find_marks(n: int, k: int, p: int, x: int, y: int, a: List[int]) -> List[int]:
    current_sum = sum(a)
    current_median = sorted(a)[(k // 2)]
    
    if current_sum > x or current_median < y:
        return [-1]
    
    remaining_tests = n - k
    remaining_sum_needed = x - current_sum
    remaining_median_needed = y
    
    min_mark = max(1, remaining_median_needed - (remaining_tests // 2))
    max_mark = min(p, remaining_median_needed + (remaining_tests // 2))
    
    if min_mark > max_mark:
        return [-1]
    
    result = [max_mark] * ((remaining_tests + 1) // 2)
    remaining_tests -= len(result)
    
    while remaining_tests > 0:
        result.append(max_mark - 1)
        remaining_tests -= 1
    
    return result

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])
    x = int(data[3])
    y = int(data[4])
    a = list(map(int, data[5:]))
    
    result = find_marks(n, k, p, x, y, a)
    
    if result == [-1]:
        print("-1")
    else:
        print(" ".join(map(str, result)))