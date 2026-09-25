import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    k = 0
    for i in range(1, n - 1):
        if a[i - 1] == a[i + 1] == 1 and a[i] == 0:
            k += 1
            a[i] = 1  # Turn on the light to simulate turning it off by the neighbor
    
    print(k)

if __name__ == "__main__":
    main()