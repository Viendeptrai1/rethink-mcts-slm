from typing import List

def max_happiness(n: int, m: int, a: List[int], subarrays: List[List[int]]) -> int:
    # Initialize a list to keep track of the number of subarrays each flower is part of
    count = [0] * n
    
    # Use prefix sums to count the number of subarrays each flower is part of
    for l, r in subarrays:
        count[l-1] += 1
        if r < n:
            count[r] -= 1
    
    # Compute the actual number of subarrays each flower is part of
    for i in range(1, n):
        count[i] += count[i-1]
    
    # Calculate the maximum possible value added to Alyona's happiness
    return sum(a[i] * count[i] for i in range(n))

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    subarrays = [[int(data[2+n+2*i]), int(data[2+n+2*i+1])] for i in range(m)]
    
    result = max_happiness(n, m, a, subarrays)
    print(result)