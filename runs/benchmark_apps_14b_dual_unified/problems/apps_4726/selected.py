def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    m = int(data[0])
    n = int(data[1])
    t = int(data[2])
    
    complexities = {
        1: lambda n: n**5,
        2: lambda n: 2**n,
        3: lambda n: n**4,
        4: lambda n: n**3,
        5: lambda n: n**2,
        6: lambda n: n * (n.bit_length() - 1),
        7: lambda n: n
    }
    
    if complexities[t](n) <= m:
        print("AC")
    else:
        print("TLE")

if __name__ == "__main__":
    main()