import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the coffee cups by caffeine content in descending order
    a.sort(reverse=True)
    
    # Initialize a list to keep track of the maximum pages that can be written each day
    max_pages_per_day = [0] * (n + 1)
    
    # Fill the max_pages_per_day array
    for i in range(1, n + 1):
        max_pages_per_day[i] = max_pages_per_day[i - 1] + max(0, a[i - 1] - (i - 1))
    
    # Use binary search to find the minimum number of days required
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if max_pages_per_day[mid] >= m:
            right = mid
        else:
            left = mid + 1
    
    # If the maximum pages that can be written in 'left' days is less than 'm', return -1
    if max_pages_per_day[left] < m:
        return -1
    
    return left

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = min_days_to_complete_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()