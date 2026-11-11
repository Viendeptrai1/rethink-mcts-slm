import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    weights = list(map(int, data[1:]))
    
    min_diff = float('inf')
    
    for T in range(1, N):
        S1 = sum(weights[:T])
        S2 = sum(weights[T:])
        diff = abs(S1 - S2)
        if diff < min_diff:
            min_diff = diff
    
    print(min_diff)

if __name__ == "__main__":
    main()