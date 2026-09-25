import sys

def main():
    x = float(sys.stdin.read().strip())
    n = int(x * 1000000)
    
    for i in range(1, 11):
        if n % i == 0:
            j = n // i
            if 1 <= j <= 10:
                print(i, j)
                return

if __name__ == "__main__":
    main()