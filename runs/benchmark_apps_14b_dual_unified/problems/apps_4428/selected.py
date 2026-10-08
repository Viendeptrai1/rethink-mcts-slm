import sys

def max_equal_sum_split(n, d):
    total_sum = sum(d)
    seen_sums = {}
    current_sum = 0
    
    for i in range(n):
        current_sum += d[i]
        if current_sum * 2 == total_sum:
            return current_sum
        seen_sums[current_sum] = i
    
    current_sum = 0
    for j in range(n - 1, -1, -1):
        current_sum += d[j]
        if current_sum * 2 == total_sum:
            return current_sum
        if (total_sum - current_sum) // 2 in seen_sums:
            return (total_sum - current_sum) // 2
    
    return 0

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:]))
    
    result = max_equal_sum_split(n, d)
    print(result)