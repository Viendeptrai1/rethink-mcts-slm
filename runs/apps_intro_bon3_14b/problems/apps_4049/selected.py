import sys

def main():
    import sys
    import math
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n = read_ints()[0]
    a1, a2, a3 = read_ints()
    b1, b2, b3 = read_ints()
    
    # Calculate the minimum number of rounds Alice can win
    min_wins = max(0, a2 - b1) + max(0, a3 - b2) + max(0, a1 - b3)
    
    # Calculate the maximum number of rounds Alice can win
    max_wins = min(a1, b2) + min(a2, b3) + min(a3, b1)
    
    print(min_wins, max_wins)

if __name__ == "__main__":
    main()