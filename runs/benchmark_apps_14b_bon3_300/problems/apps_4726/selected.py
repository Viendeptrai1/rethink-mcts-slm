import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    m = int(data[0])
    n = int(data[1])
    t = int(data[2])
    
    if t == 1:
        result = n
    elif t == 2:
        result = 1 << n  # 2^n
    elif t == 3:
        result = n ** 4
    elif t == 4:
        result = n ** 3
    elif t == 5:
        result = n ** 2
    elif t == 6:
        result = n * (n.bit_length() - 1)  # n * log2(n)
    elif t == 7:
        result = n
    
    if result <= m:
        print("AC")
    else:
        print("TLE")

if __name__ == "__main__":
    main()