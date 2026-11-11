import sys
from collections import defaultdict

def max_sum_split(n, d):
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + d[i - 1]
    
    max_sum = 0
    seen_sums = defaultdict(list)
    
    for i in range(n + 1):
        current_sum = prefix_sum[i]
        target_sum = current_sum * 2 - prefix_sum[n]
        
        if target_sum in seen_sums:
            for j in seen_sums[target_sum]:
                max_sum = max(max_sum, current_sum - prefix_sum[j])
        
        seen_sums[current_sum].append(i)
    
    return max_sum

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:]))
    
    result = max_sum_split(n, d)
    print(result)