def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    W = list(map(int, data[1:]))
    
    min_diff = float('inf')
    
    total_sum = sum(W)
    current_sum = 0
    
    for i in range(N - 1):
        current_sum += W[i]
        diff = abs(current_sum - (total_sum - current_sum))
        if diff < min_diff:
            min_diff = diff
    
    print(min_diff)

main()