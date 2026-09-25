import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a1, a2, a3 = map(int, data[1:4])
    b1, b2, b3 = map(int, data[4:7])
    
    # Calculate the maximum number of rounds Alice can win
    max_wins = min(a1, b2) + min(a2, b3) + min(a3, b1)
    
    # Calculate the minimum number of rounds Alice can win
    min_wins = max(0, a1 - b3) + max(0, a2 - b1) + max(0, a3 - b2)
    
    print(min_wins, max_wins)

if __name__ == "__main__":
    main()