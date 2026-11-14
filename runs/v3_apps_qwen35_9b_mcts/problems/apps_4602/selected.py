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
    for xi in x:
        dist_a = 2 * xi
        dist_b = 2 * (K - xi)
        total_distance += min(dist_a, dist_b)
    
    print(total_distance)

if __name__ == "__main__":
    solve()