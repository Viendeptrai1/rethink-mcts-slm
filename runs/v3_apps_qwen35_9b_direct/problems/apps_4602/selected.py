import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    x = []
    for i in range(N):
        x.append(int(data[2 + i]))
    
    total_distance = 0
    
    for i in range(N):
        xi = x[i]
        # Distance if type-A robot is used: goes from 0 to xi and back to 0
        dist_a = 2 * xi
        
        # Distance if type-B robot is used: goes from K to xi and back to K
        dist_b = 2 * (K - xi)
        
        # Choose the minimum
        total_distance += min(dist_a, dist_b)
    
    print(total_distance)

if __name__ == "__main__":
    solve()