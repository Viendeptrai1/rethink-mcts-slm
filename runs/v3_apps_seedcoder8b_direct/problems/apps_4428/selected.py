def max_equal_sum_partition(n, d):
    total_sum = sum(d)
    if total_sum % 2 != 0:
        return 0

    target_sum = total_sum // 2
    current_sum = 0
    max_sum = 0

    for i in range(n):
        current_sum += d[i]
        if current_sum == target_sum:
            max_sum = target_sum
            break
        elif current_sum > target_sum:
            break

    return max_sum

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:n+1]))
    
    result = max_equal_sum_partition(n, d)
    print(result)