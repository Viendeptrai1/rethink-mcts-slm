MOD = 998244353

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    points.sort(key=lambda p: (p[0], p[1]))
    
    total_sum = 0
    
    for i in range(N):
        min_x = points[i][0]
        max_y = points[i][1]
        
        count = 1
        
        for j in range(i + 1, N):
            if points[j][0] == min_x:
                break
            min_x = points[j][0]
            max_y = max(max_y, points[j][1])
            count += 1
        
        total_sum += count * (N - i) % MOD
    
    print(total_sum % MOD)

if __name__ == "__main__":
    solve()