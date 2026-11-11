import sys

def max_sum_split(n, d):
    total_sum = sum(d)
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    prefix_sums = [0] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + d[i - 1]
    
    seen_sums = set()
    max_sum = 0
    
    for i in range(n + 1):
        current_sum = prefix_sums[i]
        needed_sum = current_sum + target
        
        if needed_sum in seen_sums:
            max_sum = max(max_sum, current_sum)
        
        seen_sums.add(current_sum)
    
    return max_sum

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:]))
    
    result = max_sum_split(n, d)
    print(result)