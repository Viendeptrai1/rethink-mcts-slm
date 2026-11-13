import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    K = int(data[1])
    x = [int(data[i+2]) for i in range(N)]
    
    total_distance = 0
    
    for i in range(N):
        xi = x[i]
        # Distance if type-A robot is used: (xi - 0) * 2
        dist_a = xi * 2
        
        # Distance if type-B robot is used: (K - xi) * 2
        dist_b = (K - xi) * 2
        
        # Choose the minimum
        total_distance += min(dist_a, dist_b)
    
    print(total_distance)

if __name__ == "__main__":
    solve()