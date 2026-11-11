import sys

def determine_winner(n, a):
    if n == 1:
        return "BitLGM" if a[0] > 0 else "BitAryo"
    
    max_a = max(a)
    min_a = min(a)
    
    if max_a == min_a:
        return "BitLGM"
    
    if n % 2 == 1:
        return "BitLGM"
    
    return "BitAryo"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = determine_winner(n, a)
    print(result)

if __name__ == "__main__":
    main()