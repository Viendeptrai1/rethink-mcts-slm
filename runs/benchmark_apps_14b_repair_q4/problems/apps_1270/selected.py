import sys

def main():
    n = int(sys.stdin.read().strip())
    
    if n == 2:
        print(1)
        print(2)
        return
    
    k = n // 2
    if n % 2 == 0:
        print(k)
        print(" ".join(["2"] * k))
    else:
        print(k)
        print(" ".join(["2"] * (k - 1) + ["3"]))

if __name__ == "__main__":
    main()