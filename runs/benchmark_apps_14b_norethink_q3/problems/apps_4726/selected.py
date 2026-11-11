import sys

def main():
    import sys
    m, n, t = map(int, sys.stdin.readline().split())
    
    if t == 1:
        operations = 1
    elif t == 2:
        operations = 2 ** n
    elif t == 3:
        operations = n ** 4
    elif t == 4:
        operations = n ** 3
    elif t == 5:
        operations = n ** 2
    elif t == 6:
        operations = n * (n.bit_length() - 1)
    elif t == 7:
        operations = n
    
    if operations <= m:
        print("AC")
    else:
        print("TLE")

if __name__ == "__main__":
    main()