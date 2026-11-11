import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    x = list(map(int, data[2:]))
    
    total_distance = 0
    
    for i in range(N):
        distance_A = 2 * abs(x[i] - 0)
        distance_B = 2 * abs(x[i] - K)
        total_distance += min(distance_A, distance_B)
    
    print(total_distance)

if __name__ == "__main__":
    main()