def max_happiness(n, m, moods, subarrays):
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i-1] + moods[i-1]
    
    max_happiness = float('-inf')
    
    for mask in range(1 << m):
        total = 0
        for i in range(n):
            count = 0
            for j in range(m):
                if mask & (1 << j):
                    l, r = subarrays[j]
                    if l - 1 <= i < r:
                        count += 1
            total += moods[i] * count
        max_happiness = max(max_happiness, total)
    
    return max_happiness

def main():
    n, m = map(int, input().split())
    moods = list(map(int, input().split()))
    subarrays = [tuple(map(int, input().split())) for _ in range(m)]
    
    result = max_happiness(n, m, moods, subarrays)
    print(result)

if __name__ == "__main__":
    main()