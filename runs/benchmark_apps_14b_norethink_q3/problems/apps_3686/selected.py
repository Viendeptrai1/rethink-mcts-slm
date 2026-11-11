import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    targets = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    if N <= 2:
        print("success")
        return
    
    slopes = defaultdict(int)
    
    for i in range(N):
        for j in range(i+1, N):
            dx = targets[j][0] - targets[i][0]
            dy = targets[j][1] - targets[i][1]
            
            if dx == 0:
                slope = float('inf')
            else:
                slope = dy / dx
            
            slopes[slope] += 1
    
    if len(slopes) > 2:
        print("failure")
    else:
        print("success")

if __name__ == "__main__":
    main()