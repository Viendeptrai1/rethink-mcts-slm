import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    # Transform the array to -1, 0, 1 based on comparison with m
    transformed = [0] * n
    for i in range(n):
        if a[i] < m:
            transformed[i] = -1
        elif a[i] > m:
            transformed[i] = 1
    
    # Calculate prefix sums
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + transformed[i]
    
    # Count occurrences of each prefix sum
    prefix_count = defaultdict(int)
    for ps in prefix_sum:
        prefix_count[ps] += 1
    
    # Calculate the number of valid subarrays
    result = 0
    for i in range(n + 1):
        # We need prefix_sum[j] - prefix_sum[i] <= 0
        # This means prefix_sum[j] <= prefix_sum[i]
        result += prefix_count[prefix_sum[i]]
        # Subtract one because we don't want subarrays ending at i itself
        if prefix_sum[i] in prefix_count:
            prefix_count[prefix_sum[i]] -= 1
    
    print(result)

if __name__ == "__main__":
    main()