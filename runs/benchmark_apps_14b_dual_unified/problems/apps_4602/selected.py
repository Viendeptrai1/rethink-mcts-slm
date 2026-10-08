import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    x = list(map(int, data[2:2+N]))
    
    min_distance = float('inf')
    
    for i in range(1 << N):
        distance = 0
        for j in range(N):
            if i & (1 << j):
                distance += abs(x[j] - 0) * 2
            else:
                distance += abs(x[j] - K) * 2
        min_distance = min(min_distance, distance)
    
    print(min_distance)

if __name__ == "__main__":
    main()