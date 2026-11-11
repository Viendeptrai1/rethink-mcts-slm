import sys

def determine_winner(n, a):
    if n == 1:
        return "BitLGM" if a[0] > 0 else "BitAryo"
    
    if n == 2:
        if a[0] == a[1]:
            return "BitLGM"
        else:
            return "BitAryo"
    
    if n == 3:
        if a[0] == a[1] == a[2]:
            return "BitLGM"
        elif a[0] == a[1] or a[1] == a[2] or a[0] == a[2]:
            return "BitAryo"
        else:
            return "BitLGM"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    winner = determine_winner(n, a)
    print(winner)

if __name__ == "__main__":
    main()